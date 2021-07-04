import pygame as pg
from pygame import transform
import Const
from pygame.math import Vector2
from Model.GameObject.basic_game_object import Basic_Game_Object

class Basic_Attack_Object(Basic_Game_Object):
    def __init__(self, model, attacker_id, position, direction, damage, name):
        super().__init__(model, position.x, position.y, 1, 1)
        self.name = name
        self.attacker_id = attacker_id
        self.speed = direction.normalize() * Const.ARROW_SPEED
        self.damage = damage
        
    def tick(self):
        self.basic_tick()
        for player in self.model.players:
            if self.attacker_id != player.player_id\
                and player.rect.collidepoint(self.center.x, self.center.y):
                player.be_special_attacked(self)
                self.kill()

class Arrow(Basic_Attack_Object):
    def __init__(self, model, attacker_id, position, direction, damage):
        super().__init__(model, attacker_id, position, direction, damage, 'Arrow')

class Bug(Basic_Attack_Object):
    def __init__(self, model, attacker_id, position, direction, damage):
        super().__init__(model, attacker_id, position, direction, damage, 'Bug')
        self.obey_gravity = True
        self.gravity = Const.BUG_GRAVITY

class Coffee(Basic_Attack_Object):
    def __init__(self, model, attacker_id, position, direction, damage):
        super().__init__(model, attacker_id, position, direction, damage, 'Coffee')
        self.obey_gravity = True
        self.gravity = Const.COFFEE_GRAVITY

class Dos(Basic_Game_Object):
    def __init__(self, model, attacker, target):
        super().__init__(model, attacker.center.x, attacker.center.y, 1, 1)
        self.name = 'Dos'
        self.attacker = attacker
        self.direction = target.center-self.position
        self.timer = 0
        self.rounds = Const.DOS_ACTIVE_LIMIT

    def tick(self):
        self.basic_tick()
        if self.timer<=0:
            self.timer = Const.DOS_TIMER
            self.rounds -=1
            self.model.attacks.append(Arrow(self.model, self.attacker.player_id, 
                                            self.position, self.direction, Const.DOS_DAMAGE))
        self.timer -= 1
        if self.rounds<=0:
            self.kill()

class Ddos(Basic_Game_Object):
    def __init__(self, model, attacker, target):
        super().__init__(model, target.center.x, target.center.y, 1, 1)
        self.name = 'Ddos'
        self.attacker = attacker
        self.direction = Vector2(0,1) * Const.DDOS_RADIUS
        self.timer = 0
        self.rounds = Const.DDOS_ACTIVE_LIMIT

    def tick(self):
        self.basic_tick()
        if self.timer<=0:
            self.timer = Const.DDOS_TIMER
            self.rounds -= 1
            for _ in range(5):
                From = self.position - self.direction
                self.model.attacks.append(Arrow(self.model, self.attacker.player_id, 
                                            From, self.direction, Const.DDOS_DAMAGE))
                self.direction.rotate_ip(72)
        self.timer -= 1
        if self.rounds<=0:
            self.kill()

class Throw_Bug(Basic_Game_Object):
    def __init__(self, model, attacker, target):
        super().__init__(model, attacker.center.x, attacker.center.y, 1, 1)
        self.name = 'Throw_Bug'
        self.model.attacks.append(Bug(model,attacker.player_id, self.position, 
                                      Vector2(-1,-1), Const.BUG_DAMAGE))
        self.kill()

class Throw_Coffee(Basic_Game_Object):
    def __init__(self, model, attacker, target):
        super().__init__(model, attacker.center.x, attacker.center.y, 1, 1)
        self.name = 'Throw_Coffee'
        self.model.attacks.append(Coffee(model,attacker.player_id, self.position, 
                                      Vector2(-1,-1), Const.COFFEE_DAMAGE))
        self.kill()