import pygame as pg
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
                         Const.PLYAER_WIDTH,Const.PLYAER_HEIGHT)
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
                self.speed.y = -Const.PLAYER_JUMP_SPEED
        else:
            self.position += Const.PLAYER_SHIFT_SPEED / Const.FPS * Const.DIRECTION_TO_VEC2[direction]
            self.face = Const.DIRECTION_TO_VEC2[direction]
        self.clip_position()

    def tick(self):
        for key,value in self.state.items():
            if key == 'in_folder' and value == 1:
                State.invisible(self.state)
            value = max(value - 1, 0)
        self.basic_tick()
          

    def touch_item(self, item_type):
        if item_type in Const.ITEM_TYPE_LIST[0:6]:
            self.keep_item_type = item_type
        elif item_type == 'EXE':
            pass
        elif item_type == 'USB':
            State.infect(self.state)
            print(self.state)
        elif item_type == 'FIREWALL':
            State.firewall(self.state)
            print(self.state)
        elif item_type == 'GRAPHIC_CARD':
            State.graphiccard(self.state)
            print(self.state)
        elif item_type == 'FORMAT':
            State.normal(self.state)
            print(self.state)
        elif item_type == 'FOLDER_UNUSED':
            State.folder(self.state)
            print(self.state)
        elif item_type == 'CHARGE':
            pass

    def special_attack(self):
        if(self.keep_item_type == 'DOS'):
            self.model.attacks.append(Dos(self.model, self, self.model.players[(self.player_id+1)%4]))
        elif(self.keep_item_type == 'DDOS'):
            self.model.attacks.append(Ddos(self.model, self, self.model.players[(self.player_id+1)%4]))
        elif(self.keep_item_type == 'THROW_COFFEE'):
            self.model.attacks.append(Throw_Coffee(self.model, self, self.model.players[(self.player_id+1)%4]))
        elif(self.keep_item_type == 'THROW_BUG'):
            self.model.attacks.append(Throw_Bug(self.model, self, self.model.players[(self.player_id+1)%4]))
        self.keep_item_type = ''

    def be_special_attacked(self, attack):
        if attack.name == 'Arrow':
            self.blood-=attack.damage
            State.slow_down(self.state)
            print(self.state)
        if attack.name == 'Bug':
            self.blood-=attack.damage
            State.broken(self.state)
            print(self.state)
        if attack.name == 'Coffee':
            self.blood-=attack.damage
            State.broken(self.state)
            print(self.state)
        
    def be_common_attacked(self):
        self.blood -= Const.PLAYER_COMMON_ATTACK_DAMAGE

    def can_be_common_attacked(self):
        if self.state['be_common_attacked'] == 0:
            return True
        else:
            return False

    def can_be_special_attacked(self):
        if self.state['be_special_attacked'] == 0:
            return True
        else:
            return False

    def is_invisible(self):
        if self.state['invisible'] == 0:
            return False
        else:
            return True

    def can_special_attack(self):
        if self.state['special_attack'] == 0:
            return True
        else:
            return False

    def infected(self):
        if self.state['infected'] == 0:
            return False
        else:
            return True

    def in_folder(self):
        if self.state['in_folder'] == 0:
            return False
        else:
            return True
