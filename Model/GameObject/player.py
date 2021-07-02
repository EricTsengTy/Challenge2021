import pygame as pg
import Const 
from pygame.math import Vector2
from Model.GameObject.basic_game_object import Basic_Game_Object
class Player(Basic_Game_Object):
    def __init__(self, model, player_id):
        super().__init__(model,
                         Const.PLAYER_INIT_POSITION[player_id].x,
                         Const.PLAYER_INIT_POSITION[player_id].y,
                         Const.PLYAER_WIDTH,Const.PLYAER_HEIGHT)
        self.player_id = player_id
        self.max_jump = 2
        self.jump_count = 0
        self.item_id = 0 #the item_id of the item player touch, 0 for nothing
        self.blood = Const.PLAYER_FULL_BLOOD
        self.can_common_attack = True
        self.can_special_attack = True
        self.would_be_common_attacked = True
        self.would_be_special_attacked = True
        self.is_invisible = False
        self.invisible_time = 0
        self.landing = True
        self.obey_gravity = True
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

    def touch_item(self, item_type):
        if item_type in range(Const.FAN_TYPE, Const.DDOS_TYPE + 1):
            self.keep_item_type = item_type
        elif item_type == Const.EXE_TYPE:
            pass
        elif item_type == Const.USB_TYPE:
            pass
        elif item_type == Const.FIREWARM_TYPE:
            pass
        elif item_type == Const.GRAPHIC_CARD_TYPE:
            pass
        elif item_type == Const.FORMAT_TYPE:
            pass
        elif item_type == Const.FOLDER_UNUSED_TYPE:
            pass
        elif item_type == Const.CHARGE_TYPE:
            pass
        
    def can_be_common_attacked(self):
        return (not self.is_invisible) and self.would_be_common_attacked
    
    def can_be_special_attacked(self):
        return (not self.is_invisible) and self.would_be_special_attacked
        
    def be_common_attacked(self):
        self.blood -= Const.PLAYER_COMMON_ATTACK_DAMAGE

    def invisible(self, time):
        self.is_invisible = True
        self.invisible_time = time * Const.FPS


