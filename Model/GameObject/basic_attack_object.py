import pygame as pg
import Const
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
        