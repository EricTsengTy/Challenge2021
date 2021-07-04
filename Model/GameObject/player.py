import pygame as pg
import Const 
from pygame.math import Vector2
from Model.GameObject.state import *
    
class Player(pg.Rect,StatesList):
    def __init__(self, player_id):
        pg.Rect.__init__(self,(Const.PLAYER_INIT_POSITION[player_id].x,
                                   Const.PLAYER_INIT_POSITION[player_id].y,
                                   Const.PLAYER_WIDTH,Const.PLAYER_HEIGHT))
        StatesList.__init__(self)
        self.player_id = player_id
        self.max_jump = 2
        self.jump_count = 0
        self.position = Vector2(self.center)
        self.horizontal_speed = Const.PLAYER_SPEED
        self.vertical_speed = 0 # negative is up, positive is down
        self.blood = Const.PLAYER_FULL_BLOOD
        self.common_attack_range = self.inflate(Const.PLAYER_COMMON_ATTACK_SIZE, Const.PLAYER_COMMON_ATTACK_SIZE)
        self.item_type = 0 #the item_type of the item player touch, 0 for nothing
        self.keep_item_type = 0 #the item_type of the item player touch, 0 for nothing
        self.never_die = True

        # View
        self.direction = 'right'

    def move(self, direction: str):
        '''
        Move the player along the direction by its speed.
        Will automatically clip the position so no need to worry out-of-bound moving.
        '''
        # Modify position and velocity of player
        if direction=='jump':
            # player can jump only if he is falling
            if self.vertical_speed>=0 and self.jump_count < self.max_jump:
                self.jump_count += 1
                self.vertical_speed = -Const.PLAYER_JUMP_SPEED
        else:
            self.position += self.horizontal_speed / Const.FPS * Const.DIRECTION_TO_VEC2[direction] * self.multiple_of_speed()
        self.clip_position()
        self.sync(last_modify='position')

        # View
        self.direction = direction

    def move_every_tick(self):
        # keep falling
        self.position.y += self.vertical_speed/Const.FPS
        self.vertical_speed += Const.PLAYER_GRAVITY/Const.FPS
        self.clip_position()
        self.sync(last_modify='position')

    def clip_position(self):
        self.position.x = max(0, min(Const.ARENA_SIZE[0], self.position.x))
        self.position.y = max(0, min(Const.ARENA_SIZE[1], self.position.y))

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
        
    def died(self):
        self.never_die = False
        self.states_clean()
        self.be_invisible.into(Const.PLAYER_REVIVE_PROTECTION)
        # copied from __init__
        self.horizontal_speed = Const.PLAYER_SPEED
        self.vertical_speed = 0
        self.blood = Const.PLAYER_FULL_BLOOD
        self.item_type = 0
        self.keep_item_type = 0
        
    def be_common_attacked(self, damage):
        self.blood -= damage
        if self.blood <= 0:
            self.died()

    def sync(self, last_modify:str):
        if last_modify=='rect':
            self.position=Vector2(self.center)
            self.common_attack_range.center=self.center
        elif last_modify=='position':
            self.center=self.position
            self.common_attack_range.center=self.center

