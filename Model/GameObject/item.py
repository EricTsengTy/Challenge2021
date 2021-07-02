import pygame as pg
import Const

class Item(pg.Rect):
    def __init__(self, left, top, item_type):
        pg.Rect.__init__(self, (left, top, Const.ITEM_WIDTH, Const.ITEM_HEIGHT))
        self.item_type = item_type
        self.timer = 0 
        self.timer_activated = False

    def tick(self):
        if self.timer_activated:
            self.timer -= 1

    def activate(self):
        self.timer_activated = True
        self.time = 60 if self.item_type == Const.FOLDER_USED_TYPE else -1

    def is_dead(self):
        return self.timer<0
