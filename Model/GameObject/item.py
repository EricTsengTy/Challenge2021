import pygame as pg
import Const

class Item(pg.Rect):
    def __init__(self, left, top, item_id):
        pg.Rect.__init__(self, (left, top, Const.ITEM_WIDTH, Const.ITEM_HEIGHT))
        self.item_id = item_id
        self.timer = 0 
        self.timer_activated = False

    def tick(self):
        if self.timer_activated:
            self.timer -= 1
            
    def is_dead(self):
        return self.timer<0
