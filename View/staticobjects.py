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
        cls.stage = cls.stage.convert()

    def draw(self, screen):
        #screen.fill(Const.BACKGROUND_COLOR)
        screen.blit(self.stage, (0, 0))

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

'''
class View_players(__Object_base):
    images = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players' , Const.PLAYER_PICS[_i])), 
            Const.PLAYER_WIDTH,Const.PLAYER_HEIGHT
        )
        for _i in range(8)
    )
    keep_item_images = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'special_attack_keep', Const.SPECIAL_ATTACK_KEEP_PICS[_i])),
            Const.ITEM_BOX_SIZE, Const.ITEM_BOX_SIZE
        ) 
        for _i in range(6)
    )

    @classmethod
    def init_convert(cls):
        cls.images = tuple( img.convert_alpha() for img in cls.images)
        cls.keep_item_images = tuple( img.convert_alpha() for img in cls.keep_item_images)
    
    def draw(self, screen):
        for player in self.model.players:
            # player itself
            status = 0 if player.face == Const.DIRECTION_TO_VEC2['right'] else 1
            screen.blit(self.images[Const.PICS_PER_PLAYER*player.player_id + status],
                self.images[Const.PICS_PER_PLAYER*player.player_id + status].get_rect(center=player.center))

            # blood
            pg.draw.rect(screen, Const.HP_BAR_COLOR[1], [player.left, player.top-10, player.rect.width*player.blood/Const.PLAYER_FULL_BLOOD, 5])
            # empty hp bar
            pg.draw.rect(screen, Const.HP_BAR_COLOR[0], [player.left, player.top-10, player.rect.width, 5], 2)

            #item frame
            pg.draw.rect(screen, Const.ITEM_BOX_COLOR, [player.left-20, player.top-15, Const.ITEM_BOX_SIZE, Const.ITEM_BOX_SIZE], 2)
            #item
            if player.keep_item_type != '':
                screen.blit(self.keep_item_images[Const.SPECIAL_ATTACK_KEEP_TO_NUM[player.keep_item_type]],
                    self.keep_item_images[Const.SPECIAL_ATTACK_KEEP_TO_NUM[player.keep_item_type]].get_rect(topleft=(player.left-20, player.top-15)))
'''