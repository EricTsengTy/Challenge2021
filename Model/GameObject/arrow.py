import pygame as pg
import Const
import random
class arrow:
    def __init__(self, player_id, position, direction, damage):
        self.entity_type = Const.ARROW_TYPE
        self.player_id = player_id
        self.position = pg.Vector2(position)
        self.direction = direction.normalize()
        self.speed = Const.ARROW_SPEED
        self.damage = damage
        self.dead = False

    def tick(self, entities):
        self.position += self.direction * Const.ARROW_SPEED / Const.FPS
        if not pg.Rect(0, 0, Const.ARENA_SIZE[0], Const.ARENA_SIZE[1]).collidepoint(self.position.x, self.position.y):
            self.dead = True
    
    def touch(self, player):
        return self.player_id != player.player_id and player.collidepoint(self.position.x, self.position.y)

    def activate(self):
        self.dead = True

    def is_dead(self):
        return self.dead

class dos:
    def __init__(self, player_id, position, direction):
        self.entity_type = None
        self.player_id = player_id
        self.position = position
        self.direction = direction.normalize()
        self.timer = 0
        self.active_num = 0
        self.dead = False
        
    def tick(self, entities):
        if self.timer == 0:
            entities.append(arrow(self.player_id, self.position, self.direction, Const.DOS_DAMAGE))
            self.active_num += 1        
            self.timer = Const.DOS_TIMER
            if self.active_num >= Const.DOS_ACTIVE_LIMIT:
                self.dead = True
        self.timer -= 1 

    def touch(self, players):
        return False

    def is_dead(self):
        return self.dead
