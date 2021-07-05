import pygame as pg
import os.path
import math

import Model.GameObject.player as model_player
from View.utils import scale_surface, load_image, resize_surface
import Const

class __Object_base():
    images = tuple()

    @classmethod
    def init_convert(cls):
        cls.images = tuple(img.convert_alpha() for img in images)
    
    def __init__(self, model):
        self.model = model

class View_players(__Object_base):
    images = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players' ,Const.PLAYER_PICS[_i])), 
            Const.PLAYER_WIDTH,Const.PLAYER_HEIGHT
        )
        for _i in range(8)
    )

    @classmethod
    def init_convert(cls):
        cls.images = tuple( img.convert_alpha() for img in cls.images)
        cls.movement = 0
    
    def draw(self, screen):
        for player in self.model.players:
            # player itself
            status = 0 if player.face == Const.DIRECTION_TO_VEC2['right'] else 1
            screen.blit(self.images[Const.PICS_PER_PLAYER*player.player_id + status], self.images[Const.PICS_PER_PLAYER*player.player_id + status].get_rect(center=player.center))

            # blood
            pg.draw.rect(screen, Const.HP_BAR_COLOR[1], [player.left, player.top-10, player.rect.width*player.blood/Const.PLAYER_FULL_BLOOD, 5])
            # empty hp bar
            pg.draw.rect(screen, Const.HP_BAR_COLOR[0], [player.left, player.top-10, player.rect.width, 5], 2)

            #item
            pg.draw.rect(screen, Const.ITEM_BOX_COLOR, [player.left-20, player.top-20, 15, 15], 2)
            
