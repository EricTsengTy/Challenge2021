import pygame as pg
from pygame import transform
import Const
from pygame.math import Vector2
from Model.GameObject.basic_game_object import Basic_Game_Object
from Model.GameObject.arrow import Arrow
class Dos(Basic_Game_Object):
    def __init__(self, model, attacker, target):
        super().__init__(model, attacker.center.x, attacker.center.y, 1, 1)
        self.name = 'Dos'
        self.model = model
        self.attacker = attacker
        self.direction = target.center-self.position
        self.timer = 0
        self.rounds = Const.DOS_ACTIVE_LIMIT

    def tick(self):
        self.basic_tick()
        if self.timer<=0:
            self.timer = 60
            self.model.attacks.append(Arrow(self.model, self.attacker.player_id, 
                                            self.position, self.direction, Const.DOS_DAMAGE))
        self.timer -= 1
