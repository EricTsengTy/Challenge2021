import pygame as pg
import os.path
import math

import Model.GameObject.player as model_player
from View.utils import scale_surface, load_image, resize_surface, rotate_surface
from pygame.math import Vector2
import Const
class __Object_base():
    frames = tuple()

    
    @classmethod
    def init_convert(cls):
        cls.frames = tuple( _frame.convert_alpha() for _frame in cls.frames)

    def __init__(self, delay_of_frames):
        self._timer = 0
        self.delay_of_frames = delay_of_frames
        self.frame_index_to_draw = 0
    
    def update(self):
        self._timer += 1
        
        if self._timer % self.delay_of_frames == 0:
            self.frame_index_to_draw = (self.frame_index_to_draw + 1) % len(self.frames)
    
    def draw(self, screen, pos):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(center=pos),
        )
        self.update()

class View_Bug(__Object_base):
    frames = tuple(
        pg.transform.rotate(
            resize_surface(
                load_image(os.path.join(Const.IMAGE_PATH, 'attack', 'attack_bug.png')),
                Const.BUG_WIDTH, Const.BUG_HEIGHT
            ), 72 * _i
        )
        for _i in range(5)
    )

    @classmethod
    def init_convert(cls):
        cls.frames = tuple(_frame.convert_alpha() for _frame in cls.frames)
    
    def __init__(self, delay_of_frames):
        self.delay_of_frames = delay_of_frames

    def draw(self, screen, pos, timer):
        self.frame_index_to_draw = (timer // self.delay_of_frames) % len(self.frames)
        
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(center=pos),
        )


class View_Coffee(__Object_base):
    frames = tuple(
                pg.transform.rotate(
                    scale_surface(
                        load_image(os.path.join(Const.IMAGE_PATH, 'attack', f'attack_coffee{_i+1}.png'))
                        , 0.5
                    ), 72 * _i
                )
                for _i in range(5)
            )

    @classmethod
    def init_convert(cls):
        cls.frames = tuple(_frame.convert_alpha() for _frame in cls.frames)
    
    def __init__(self, delay_of_frames):
        self.delay_of_frames = delay_of_frames

    def draw(self, screen, pos, timer):
        self.frame_index_to_draw = (timer // self.delay_of_frames) % len(self.frames)
        
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(center=pos),
        )
    

    