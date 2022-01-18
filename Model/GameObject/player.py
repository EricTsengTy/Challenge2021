import pygame as pg
import random
from pygame.display import mode_ok, set_allow_screensaver
from pygame.event import Event
from pygame.mixer import fadeout
import Const 
from pygame.math import Vector2
from Model.GameObject.basic_game_object import Basic_Game_Object
from Model.GameObject.item import Item
from Model.GameObject.special_attack import *
import Model.GameObject.state as State
from EventManager.EventManager import *

class Player(Basic_Game_Object):
    def __init__(self, model, player_id, name, is_AI):
        super().__init__(model,
                         Const.PLAYER_INIT_POSITION[player_id].x,
                         Const.PLAYER_INIT_POSITION[player_id].y,
                         Const.PLAYER_WIDTH,Const.PLAYER_HEIGHT)
        self.player_id = player_id
        self.max_jump = 2
        self.jump_count = self.max_jump

        self.enhance_blood = Const.PLAYER_FULL_BLOOD
        self.enhance_common_attack_damage = Const.PLAYER_COMMON_ATTACK_DAMAGE
        self.enhance_fireball_damage = Const.FIREBALL_DAMAGE
        self.enhance_special_attack_timer = Const.PLAYER_SPECIAL_ATTACK_TIMER
        self.blood = self.enhance_blood
        self.special_attack_timer = self.enhance_special_attack_timer

        self.state = State.init()
        self.obey_gravity = True
        self.keep_item_type = ''
        self.tmp_keep_item_type = ''
        self.can_leave_screen = False
        self.face = Const.DIRECTION_TO_VEC2['right']
        self.death = 0
        self.common_attack_timer = 0
        self.special_attack_delay = -1 # -1 for no special attack
        self.standing_tick = 0
        self.score = 0
        self.color = Const.COLOR_TABLE[player_id]
        self.color_index = player_id
        self.player_name = name
        self.is_AI = is_AI
        self.walk_to = {'walking':False, 'end':None}

    @property
    def common_attack_range(self):
        attack_range = self.rect.inflate(Const.PLAYER_COMMON_ATTACK_SIZE, Const.PLAYER_COMMON_ATTACK_SIZE)
        width = attack_range.width
        attack_range = attack_range.inflate(-width/2, 0)
        attack_range.move_ip(self.face * (width/4))
        return attack_range

    def move(self, direction: str):
        '''
        Move the player along the direction by its speed.
        Will automatically clip the position so no need to worry out-of-bound moving.
        '''
        # Modify position and velocity of player
        self.standing_tick = 0
        if direction=='jump':
            # player can jump only if he is falling
            if self.jump_count < self.max_jump:
                self.jump_count += 1
                self.speed.y = -Const.PLAYER_JUMP_SPEED * self.speed_adjust()
        else:
            self.position += Const.PLAYER_SHIFT_SPEED * self.speed_adjust() / Const.FPS * Const.DIRECTION_TO_VEC2[direction]
            self.face = Const.DIRECTION_TO_VEC2[direction]
        self.clip_position()

    def tick(self):
        if self.jump_count == 0:
            self.standing_tick +=1
        else: self.standing_tick = 0
        for key,value in self.state.items():
            if key == 'in_folder' and value == 1:
                State.invisible(self.state)
            self.state[key] = max(value-1, 0)
        
        self.special_attack_timer = max(self.special_attack_timer - self.special_attack_speed_adjust(), 0)
        self.common_attack_timer = max(self.common_attack_timer - 1, 0)
        self.special_attack_delay = max(self.special_attack_delay - 1, -1)
        if self.special_attack_delay == 0:
            self.special_attack()
        
        if self.in_folder():
            return
        self.basic_tick()
        
        #landing
        landing_detector = pg.Rect(0,0,self.rect.width/3,5)
        landing_detector.center = self.rect.midbottom
        collided = landing_detector.collidelist([ground.hitbox for ground in self.model.grounds])
        collided = self.model.grounds[collided] if collided!=-1 else None
        if self.speed.y>0 and collided!=None:
            self.bottom = collided.top
            self.speed.y = 0
            self.jump_count = 0
        self.clip_position()

    def die(self):
        self.state = State.init()
        State.invisible(self.state)
        self.position = Const.PLAYER_INIT_POSITION[self.player_id]
        self.blood = self.enhance_blood
        self.death += 1
        self.keep_item_type = ''
        self.face = Const.DIRECTION_TO_VEC2['right']
        self.jump_count = 0
        self.model.ev_manager.post(EventPlayerDie(self.player_id))

    def add_score(self, s):
        self.score += s

    def count_score(self, attacker, damage):
        # count how much score that attacker earn
        attacker.add_score(damage)
        if self.blood <= 0:
            attacker.add_score(Const.SCORE_KILL_OTHER + self.blood)
            self.die()

    def touch_item(self, item):
        item_type = item.item_type
        if item_type in Const.ITEM_KEEP_LIST:
            self.keep_item_type = item_type
            self.special_attack_timer = 0
        elif item_type == 'EXE':
            self.score += 300
            self.model.ev_manager.post(EventHelloWorld())
        elif item_type == 'USB':
            State.infect(self.state)
        elif item_type == 'FIREWALL':
            State.firewall(self.state)
        elif item_type == 'GRAPHIC_CARD':
            State.graphiccard(self.state)
        elif item_type == 'FORMAT':
            self.state = State.init()
        elif item_type == 'FOLDER_UNUSED':
            self.center = item.center
            State.folder(self.state)
        elif item_type == 'CHARGE':
            self.blood = min(self.blood+Const.CHARGE_BLOOD, self.enhance_blood)

        self.model.ev_manager.post(EventGetProp(self.player_id, item_type))


    def special_attack(self):
        if self.special_attack_timer > 0: return
        if self.special_attack_delay == -1:
            self.special_attack_delay = Const.PLAYER_SPECIAL_ATTACK_DELAY
            self.tmp_keep_item_type = self.keep_item_type
            self.keep_item_type = ''
            if self.tmp_keep_item_type != 'THROW_COFFEE' and self.tmp_keep_item_type != 'THROW_BUG':
                self.model.ev_manager.post(EventSpecialAttackMovement(self.player_id, self.tmp_keep_item_type)) 
            return
        if self.special_attack_delay > 0: return
        if self.tmp_keep_item_type == 'THROW_COFFEE' or self.tmp_keep_item_type == 'THROW_BUG':
            self.model.ev_manager.post(EventSpecialAttackMovement(self.player_id, self.tmp_keep_item_type)) 
            

        if(self.tmp_keep_item_type == 'DOS'):
            self.model.attacks.append(Dos(self.model, self, self.model.players[self.__nearest_target()]))
        elif(self.tmp_keep_item_type == 'DDOS'):
            self.model.attacks.append(Ddos(self.model, self, self.model.players[self.__nearest_target()]))
        elif(self.tmp_keep_item_type == 'THROW_COFFEE'):
            self.model.attacks.append(Throw_Coffee(self.model, self, self.model.players[(self.player_id+1)%4]))
        elif(self.tmp_keep_item_type == 'THROW_BUG'):
            self.model.attacks.append(Throw_Bug(self.model, self, self.model.players[(self.player_id+1)%4]))
        elif(self.tmp_keep_item_type == ''):
            self.model.attacks.append(Cast_Fireball(self.model, self))
        elif(self.tmp_keep_item_type == 'FAN'):
            self.model.attacks.append(Cast_Tornado(self.model, self))
        elif(self.tmp_keep_item_type == 'LIGHTNING'):
            self.model.attacks.append(Cast_Lightning(self.model, self))
        self.tmp_keep_item_type = ''
        self.special_attack_timer = self.enhance_special_attack_timer
        self.special_attack_delay = -1


    def be_special_attacked(self, attack):
        # effect (excpet damage) of all sepcial attack
        if attack.name == 'Arrow':
            State.slow_down(self.state)
        elif attack.name == 'Bug':
            State.broken(self.state, Const.BROKEN_TIME_BUG)
        elif attack.name == 'Coffee':
            State.broken(self.state, Const.BROKEN_TIME_COFFEE)
        elif attack.name == 'Tornado':
            pass
        elif attack.name == 'Fireball':
            pass
        elif attack.name == 'Lightning':
            pass
            
        # damage of special attack
        self.blood -= attack.damage

        self.count_score(attack.attacker, attack.damage)
        # self.model.ev_manager.post(EventBeAttacked(self.player_id))
        # add in special_attack.py by View
        
        
    def be_common_attacked(self, attacker):
        if attacker.infection():
            State.infect(self.state)
        damage = attacker.enhance_common_attack_damage * attacker.damage_adjust()
        self.blood -= damage
        self.model.ev_manager.post(EventBeAttacked(self.player_id))
        self.count_score(attacker, damage)
    
    def __random_target(self):
        player_id_list = [_ for _ in range(Const.PLAYER_NUMBER)]
        player_id_list.remove(self.player_id)
        return random.choice(player_id_list)

    def __nearest_target(self):
        player_id_list = [_ for _ in range(Const.PLAYER_NUMBER)]
        player_id_list.remove(self.player_id)
        for player_id in player_id_list:
            if not self.model.players[player_id].can_be_special_attacked():
                player_id_list.remove(player_id)
        if len(player_id_list) == 0:
            player_id_list = [_ for _ in range(Const.PLAYER_NUMBER)]
            player_id_list.remove(self.player_id)

        ret_player_id = player_id_list[0]    
        min_dis = (self.position - self.model.players[ret_player_id].position).length()
        for player_id in player_id_list[1:]:
            if (self.position - self.model.players[player_id].position).length() < min_dis:
                ret_player_id = player_id
                min_dis = (self.position - self.model.players[player_id].position).length()
        return ret_player_id

    def enhance(self, enhancement):
        self.enhance_blood *= (1 + 0.01 * enhancement[0])
        self.blood = self.enhance_blood
        self.enhance_common_attack_damage += enhancement[1]
        self.enhance_fireball_damage *= (1 + 0.01 * enhancement[2])
        self.enhance_special_attack_timer *= (1 - 0.01 * enhancement[3])
        self.special_attack_timer = self.enhance_special_attack_timer
    
    def can_be_common_attacked(self):
        if self.state['be_common_attacked'] == 0: return True
        else: return False

    def can_be_special_attacked(self):
        if self.state['be_special_attacked'] == 0: return True
        else: return False

    def is_invisible(self):
        if self.state['invisible'] == 0: return False
        else: return True

    def can_special_attack(self):
        if self.state['special_attack'] == 0: return True
        else: return False

    def infection(self):
        if self.state['infection'] == 0: return False
        else: return True

    def in_folder(self):
        if self.state['in_folder'] == 0: return False
        else: return True

    def damage_adjust(self):
        if self.state['infected_common_attack'] == 0: return 1
        else: return Const.PLAYER_COMMON_ATTACK_DAMAGE_ADJUST

    def speed_adjust(self):
        if self.state['slow_move_speed'] == 0: return 1
        else: return Const.PLAYER_SPEED_ADJUST

    def special_attack_speed_adjust(self):
        if self.state['fast_special_attack_speed'] == 0: return 1
        else: return 2;

    def is_standing(self):
        return self.standing_tick>5
    
    def change_color(self, color):
        self.color = color

    def can_common_attack(self):
        if self.common_attack_timer > 0 or self.in_folder(): return False
        else: return True
