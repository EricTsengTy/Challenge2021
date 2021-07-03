import pygame as pg
from pygame.display import set_allow_screensaver
import Const 
import copy
from pygame.math import Vector2
class Basic_Game_Object:
    def __init__(self, model, left, top, width, height):
        self.model = model
        self.__rect = pg.Rect(left, top, width, height)
        self.__position = Vector2(self.__rect.topleft)
        self.speed = Vector2(0.0,0.0)
        self.obey_gravity = False
        self.gravity = 0
        self.landing = False
        self.__death = False

    def clip_position(self):
        self.x = max(0, min(Const.ARENA_SIZE[0], self.x))
        self.y = max(0, min(Const.ARENA_SIZE[1], self.y))

    def basic_tick(self):
        
        if self.obey_gravity:
            self.speed.y += Const.PLAYER_GRAVITY/Const.FPS
        
        self.position += self.speed / Const.FPS

        if self.landing:
            collided = self.rect.collidelist([ground.rect for ground in self.model.grounds])
            collided = self.model.grounds[collided] if collided!=-1 else None
            if self.speed.y>0 and collided!=None and collided.bottom>self.rect.bottom>collided.top:
                self.bottom = collided.top
                self.speed.y = 0
                self.jump_count = 0
        self.clip_position()
    
    def tick(self):
        self.basic_tick()
    
    def kill(self):
        self.__death = True

    def killed(self):
        return self.__death

    @property
    def left(self):
        return self.__rect.left
    @left.setter
    def left(self, value):
        self.__rect.left = value
        self.__position = Vector2(self.__rect.topleft)

    @property
    def right(self):
        return self.__rect.right
    @right.setter
    def right(self, value):
        self.__rect.right = value
        self.__position = Vector2(self.__rect.topleft)
    
    @property
    def top(self):
        return self.__rect.top
    @top.setter
    def top(self, value):
        self.__rect.top = value
        self.__position = Vector2(self.__rect.topleft)
    
    @property
    def bottom(self):
        return self.__rect.bottom
    @bottom.setter
    def bottom(self, value):
        self.__rect.bottom = value
        self.__position = Vector2(self.__rect.topleft)

    @property
    def center(self):
        return Vector2(self.__rect.center)
    @center.setter
    def center(self, value):
        self.__rect.center = value
        self.__position = Vector2(self.__rect.topleft)
    
    @property
    def position(self):
        return copy.deepcopy(self.__position)
    @position.setter
    def position(self, value):
        self.__position = value
        self.__rect.topleft = self.__position

    @property
    def x(self):
        return self.__position.x
    @x.setter
    def x(self, value):
        self.__position.x = value
        self.__rect.topleft = self.__position
    
    @property
    def y(self):
        return self.__position.y
    @y.setter
    def y(self, value):
        self.__position.y = value
        self.__rect.topleft = self.__position

    @property
    def rect(self):
        return self.__rect
    @rect.setter
    def rect(self, value):
        self.__rect = value
        self.__position = Vector2(self.__rect.topleft)



