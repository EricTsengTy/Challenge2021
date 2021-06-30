import pygame as pg
import Const

class Item(pg.Rect):
    def __init__(self, left, top, item_id):
        pg.Rect.__init__(self, (left, top, Const.ITEM_WIDTH, Const.ITEM_HEIGHT))
        self.item_id = item_id
        self.timer = 0 

    def touch(self, players):
        for player in players:
            if self.colliderect(player):
                return player
        return None
