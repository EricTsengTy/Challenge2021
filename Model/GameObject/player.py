import pygame as pg
from pygame.display import mode_ok
from pygame.mixer import fadeout
import Const 
from pygame.math import Vector2
from Model.GameObject.basic_game_object import Basic_Game_Object
from Model.GameObject.item import Item
from Model.GameObject.special_attack import *

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
        self.can_common_attack = True
        self.can_special_attack = True
        self.would_be_common_attacked = True
        self.would_be_special_attacked = True
        self.is_invisible = False
        self.invisible_time = 0
        self.landing = True
        self.obey_gravity = True
        self.keep_item_type = ''


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
        self.clip_position()

    def tick(self):
        self.basic_tick()
        self.invisible_time -= 1
        if self.invisible_time<=0:
            self.is_invisible = False
            self.invisible_time = 0

    def touch_item(self, item_type):
        if item_type in Const.ITEM_TYPE_LIST[0:6]:
            self.keep_item_type = item_type
        elif item_type == 'EXE':
            pass
        elif item_type == 'USB':
            pass
        elif item_type == 'FIREWARM':
            pass
        elif item_type == 'GRAPHIC_CARD':
            pass
        elif item_type == 'FORMAT':
            pass
        elif item_type == 'FOLDER_UNUSED':
            self.invisible(3)
            
        elif item_type == 'CHARGE':
            pass

    def special_attack(self):
        if(self.keep_item_type == 'DOS'):
            self.model.attacks.append(Dos(self.model, self, self.model.players[(self.player_id+1)%4]))
        self.keep_item_type = ''

    def be_special_attacked(self, attack):
        if attack.name == 'Arrow':
            self.blood-=attack.damage
    
    def can_be_common_attacked(self):
        return (not self.is_invisible) and self.would_be_common_attacked
    
    def can_be_special_attacked(self):
        return (not self.is_invisible) and self.would_be_special_attacked
        
    def be_common_attacked(self):
        self.blood -= Const.PLAYER_COMMON_ATTACK_DAMAGE

    def invisible(self, time):
        self.is_invisible = True
        self.invisible_time = time * Const.FPS


