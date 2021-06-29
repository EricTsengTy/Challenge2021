import pygame as pg

class Block(pg.Rect):
    def __init__(self, left, top, width, height):
        pg.Rect.__init__(self, (left, top, width, height)) 
