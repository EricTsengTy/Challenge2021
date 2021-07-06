import pygame as pg

from View.utils import scale_surface, load_image, resize_surface
import Const

class Animation_base():
    def __init__(self, delay_of_frames, **pos):
        self._timer = 0
        self.expired = False

class Animation_raster():
    frames = tuple()

    @classmethod
    def init_convert(cls):
        cls.frames = tuple( _frame.convert_alpha() for _frame in cls.frames)

    def __init__(self, delay_of_frames, expire_time, **pos):
        self._timer = 0
        self.delay_of_frames = delay_of_frames
        self.frame_index_to_draw = 0
        self.expire_time = expire_time
        self.expired = False
    
    def update(self):
        self._timer += 1

        if self._timer == self.expire_time:
            self.expire = True
        elif self._timer % self.delay_of_frames == 0:
            self.frame_index_to_draw = (self.frame_index_to_draw + 1) % len(self.frames)

    def draw(self, screen, update=True):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(**self.pos),
        )
        
        if update: self.update()