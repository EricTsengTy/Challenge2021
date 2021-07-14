import pygame as pg
import os.path
import math

import Model.GameObject.player as model_player
from View.utils import scale_surface, load_image, resize_surface, rotate_surface
from pygame.math import Vector2
import Const

class __Object_base():
    images = tuple()

    @classmethod
    def init_convert(cls):
        cls.images = tuple(img.convert_alpha() for img in images)
    
    def __init__(self, model):
        self.model = model

class View_stage(__Object_base):
    stage = resize_surface(load_image(os.path.join(Const.IMAGE_PATH, 'stage', 'stage.png')),
        Const.ARENA_SIZE[0], Const.ARENA_SIZE[1])

    @classmethod
    def init_convert(cls):
        cls.stage = cls.stage.convert_alpha()

    def draw(self, screen):
        #screen.fill(Const.BACKGROUND_COLOR)
        screen.blit(self.stage, (0, 0))

class View_platform(__Object_base):
    block = resize_surface(load_image(os.path.join(Const.IMAGE_PATH, 'floor', 'floor_block.png')),
        Const.GROUND_SIZE, Const.GROUND_SIZE)


    @classmethod
    def init_convert(cls):
        cls.block = cls.block.convert_alpha()

    def draw(self, screen):
        for ground in Const.GROUND_POSITION[:-1]:
            #(left, top, width, height)
            block_num = ground[2] // Const.GROUND_SIZE
            for _i in range(block_num):
                screen.blit(self.block, self.block.get_rect(topleft=(ground[0] + Const.GROUND_SIZE * _i , ground[1])))

class View_Arrow(__Object_base):
    images = tuple(
        rotate_surface(
            resize_surface(
                load_image(os.path.join(Const.IMAGE_PATH, 'attack', 'attack_dos.png')),
                Const.ARROW_SIZE ,Const.ARROW_SIZE
            ), 180 + 72*_i
        )
        for _i in range(5)
    )

    @classmethod
    def init_convert(cls):
        cls.images = tuple( img.convert_alpha() for img in cls.images)
    
    def draw(self, screen, pos, speed):
        angle = round(Vector2().angle_to(speed))
        if angle in [90,162,-54,126,18]:
            screen.blit(self.images[(5-((angle+270)//72))%5], self.images[(5-((angle+270)//72))%5].get_rect(center=pos))
        else:
            img = rotate_surface(self.images[0], -angle+90)
            screen.blit(img, img.get_rect(center=pos))

class View_Lightning(__Object_base):
    images = tuple(
        rotate_surface(
            resize_surface(
                load_image(os.path.join(Const.IMAGE_PATH, 'attack', 'attack_lightning.png')),
                Const.LIGHTNING_SIZE ,Const.LIGHTNING_SIZE
            ), -90 - 45*_i
        )
        for _i in range(8)
    )

    @classmethod
    def init_convert(cls):
        cls.images = tuple( img.convert_alpha() for img in cls.images)
    
    def draw(self, screen, pos, dist):
        for _i in range(8):
            screen.blit(self.images[_i], self.images[_i].get_rect(center=(pos - dist * Vector2(1, 0).rotate(45 * _i))))

class View_Item(__Object_base):
    images = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'prop', Const.PROP_PICS[_i])),
            Const.ITEM_WIDTH, Const.ITEM_HEIGHT
        )
        for _i in range(13)
    )
    prop_image = resize_surface(
        load_image(os.path.join(Const.IMAGE_PATH, 'prop', 'prop.png')),
        Const.ITEM_WIDTH//5, Const.ITEM_HEIGHT//5
    )
    @classmethod
    def init_convert(cls):
        cls.images = tuple( img.convert_alpha() for img in cls.images)
        cls.prop_image = cls.prop_image.convert_alpha()
    def draw(self, screen, rect, item_type):
        _pic = Const.ITEM_TYPE_LIST.index(item_type)
        screen.blit(self.images[_pic], self.images[_pic].get_rect(center=rect.center))
        screen.blit(self.prop_image, self.prop_image.get_rect(bottomleft=rect.bottomleft))

def init_staticobjects():
    View_stage.init_convert()
    View_platform.init_convert()
    View_Arrow.init_convert()
    View_Lightning.init_convert()
    View_Item.init_convert()