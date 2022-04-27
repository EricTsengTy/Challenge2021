import pygame as pg
import Const
from Model.GameObject.basic_game_object import Basic_Game_Object

class Item(Basic_Game_Object):
    def __init__(self, model, left, top, item_type):
        super().__init__(model, left, top, Const.ITEM_WIDTH, Const.ITEM_HEIGHT)
        self.item_type = item_type

    def tick(self):
        for player in self.model.players:
            if player.rect.colliderect(self.rect):
                player.touch_item(self)
                self.kill()
