import pygame as pg
import Const
from Model.GameObject.basic_game_object import Basic_Game_Object

class Item(Basic_Game_Object):
    def __init__(self, model, left, top, item_type):
        super().__init__(model, left, top, Const.ITEM_WIDTH, Const.ITEM_HEIGHT)
        self.item_type = item_type
        self.timer = 0 
        self.timer_activated = False

    def tick(self):
        if self.timer_activated:
            self.timer -= 1

    def activate(self):
        self.timer_activated = True
        self.time = 60 if self.item_type == Const.FOLDER_UNUSED_TYPE else -1

    def is_dead(self):
        return self.timer<0
