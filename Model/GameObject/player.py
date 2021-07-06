import pygame as pg
import random
from pygame.display import mode_ok
from pygame.mixer import fadeout
import Const 
from pygame.math import Vector2
from Model.GameObject.basic_game_object import Basic_Game_Object
from Model.GameObject.item import Item
from Model.GameObject.special_attack import *
import Model.GameObject.state as State

class Player(Basic_Game_Object):
    def __init__(self, model, player_id):
        super().__init__(model,
                         Const.PLAYER_INIT_POSITION[player_id].x,
                         Const.PLAYER_INIT_POSITION[player_id].y,
                         Const.PLAYER_WIDTH,Const.PLAYER_HEIGHT)
        self.player_id = player_id
        self.max_jump = 2
        self.jump_count = 0
        self.blood = Const.PLAYER_FULL_BLOOD
        self.state = State.init()
        self.landing = True
        self.obey_gravity = True
        self.keep_item_type = ''
        self.can_leave_screen = False
        self.face = Const.DIRECTION_TO_VEC2['right']
        self.death = 0
        self.special_attack_timer = Const.PLAYER_SPECIAL_ATTACK_TIMER

    @property
    def common_attack_range(self):
        return self.rect.inflate(Const.PLAYER_COMMON_ATTACK_SIZE, Const.PLAYER_COMMON_ATTACK_SIZE)

    def move(self, direction: str):
        '''
        Move the player along the direction by its speed.
        Will automatically clip the position so no need to worry out-of-bound moving.
        '''
        # Modify position and velocity of player
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
        if self.blood <= 0:
            self.state = State.init()
            State.invisible(self.state)
            self.position = Const.PLAYER_INIT_POSITION[self.player_id]
            self.blood = Const.PLAYER_FULL_BLOOD
            self.death += 1
            return
        for key,value in self.state.items():
            if key == 'in_folder' and value == 1:
                State.invisible(self.state)
            self.state[key] = max(value-1, 0)
        
        if self.state['fast_special_attack_speed'] == 1:
            self.special_attack_timer = max(self.special_attack_timer - 2, 0)
        else :
            self.special_attack_timer = max(self.special_attack_timer - 1, 0)
        
        if self.in_folder():
            return
        self.basic_tick()
          

    def touch_item(self, item_type):
        if item_type in Const.ITEM_TYPE_LIST[0:6]:
            self.keep_item_type = item_type
            self.special_attack_timer = 0
        elif item_type == 'EXE':
            pass
        elif item_type == 'USB':
            State.infect(self.state)
        elif item_type == 'FIREWALL':
            State.firewall(self.state)
        elif item_type == 'GRAPHIC_CARD':
            State.graphiccard(self.state)
        elif item_type == 'FORMAT':
            State.normal(self.state)
        elif item_type == 'FOLDER_UNUSED':
            State.folder(self.state)
        elif item_type == 'CHARGE':
            pass

    def special_attack(self):
        if self.special_attack_timer > 0: return
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

    def be_special_attacked(self, attack):
        if attack.name == 'Arrow':
            self.blood-=attack.damage
            State.slow_down(self.state)
        if attack.name == 'Bug':
            self.blood-=attack.damage
            State.broken(self.state)
        if attack.name == 'Coffee':
            self.blood-=attack.damage
            State.broken(self.state)
        
    def be_common_attacked(self, attacker):
        if attacker.infection():
            State.infect(self.state)
        self.blood -= Const.PLAYER_INFECTED_COMMON_ATTACK_DAMAGE * self.damage_adjust()

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
