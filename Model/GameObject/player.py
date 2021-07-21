import pygame as pg
import random
from pygame.display import mode_ok, set_allow_screensaver
from pygame.mixer import fadeout
import Const 
from pygame.math import Vector2
from Model.GameObject.basic_game_object import Basic_Game_Object
from Model.GameObject.item import Item
from Model.GameObject.special_attack import *
import Model.GameObject.state as State
from EventManager.EventManager import *

class Player(Basic_Game_Object):
    def __init__(self, model, player_id):
        super().__init__(model,
                         Const.PLAYER_INIT_POSITION[player_id].x,
                         Const.PLAYER_INIT_POSITION[player_id].y,
                         Const.PLAYER_WIDTH,Const.PLAYER_HEIGHT)
        self.player_id = player_id
        self.max_jump = 2
        self.jump_count = self.max_jump
        self.blood = Const.PLAYER_FULL_BLOOD
        self.state = State.init()
        self.obey_gravity = True
        self.keep_item_type = ''
        self.can_leave_screen = False
        self.face = Const.DIRECTION_TO_VEC2['right']
        self.death = 0
        self.special_attack_timer = Const.PLAYER_SPECIAL_ATTACK_TIMER
        self.common_attack_timer = 0
        self.special_attack_delay = -1 # -1 for no special attack
        self.standing_tick = 0
        self.score = 0

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
            if self.speed.y>=0 and self.jump_count < self.max_jump:
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
        collided = landing_detector.collidelist([ground.rect for ground in self.model.grounds])
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
        self.blood = Const.PLAYER_FULL_BLOOD
        self.death += 1
        self.keep_item_type = ''
        self.face = Const.DIRECTION_TO_VEC2['right']
        self.jump_count = 0

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
        if item_type in Const.ITEM_TYPE_LIST[0:6]:
            self.keep_item_type = item_type
            self.special_attack_timer = 0
        elif item_type == 'EXE':
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
            self.blood = min(self.blood+100, Const.PLAYER_FULL_BLOOD)

    def special_attack(self):
        if self.special_attack_timer > 0: return
        if self.special_attack_delay == -1:
            self.special_attack_delay = Const.PLAYER_SPECIAL_ATTACK_DELAY
            return
        if self.special_attack_delay > 0: return
        
        self.model.ev_manager.post(EventSpecialAttackMovement(self.player_id, self.keep_item_type))

        if(self.keep_item_type == 'DOS'):
            self.model.attacks.append(Dos(self.model, self, self.model.players[self.__random_target()]))
        elif(self.keep_item_type == 'DDOS'):
            self.model.attacks.append(Ddos(self.model, self, self.model.players[self.__random_target()]))
        elif(self.keep_item_type == 'THROW_COFFEE'):
            self.model.attacks.append(Throw_Coffee(self.model, self, self.model.players[(self.player_id+1)%4]))
        elif(self.keep_item_type == 'THROW_BUG'):
            self.model.attacks.append(Throw_Bug(self.model, self, self.model.players[(self.player_id+1)%4]))
        elif(self.keep_item_type == ''):
            self.model.attacks.append(Cast_Fireball(self.model, self))
        elif(self.keep_item_type == 'FAN'):
            self.model.attacks.append(Cast_Tornado(self.model, self))
        elif(self.keep_item_type == 'LIGHTNING'):
            self.model.attacks.append(Cast_Lightning(self.model, self))
        self.keep_item_type = ''
        self.special_attack_timer = Const.PLAYER_SPECIAL_ATTACK_TIMER
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
            
        # damage of spcail attack
        self.blood-=attack.damage

        self.count_score(attack.attacker, attack.damage)
        self.model.ev_manager.post(EventBeAttacked(self.player_id))
        
        
    def be_common_attacked(self, attacker):
        if attacker.infection():
            State.infect(self.state)
        self.blood -= Const.PLAYER_COMMON_ATTACK_DAMAGE * self.damage_adjust()
        self.count_score(attacker, Const.PLAYER_COMMON_ATTACK_DAMAGE * self.damage_adjust())
        self.model.ev_manager.post(EventBeAttacked(self.player_id))
    
    def __random_target(self):
        player_id_list = [_ for _ in range(Const.PLAYER_NUMBER)]
        player_id_list.remove(self.player_id)
        return random.choice(player_id_list)

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

