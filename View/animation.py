import pygame as pg

from View.utils import scale_surface, load_image, resize_surface
import Const

class Animation_base():
    def __init__(self, delay_of_frames, **pos):
        self._timer = 0
        self.expired = False

