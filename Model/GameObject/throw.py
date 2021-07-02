import pygame as pg
import Const

class throw(pg.Rect):
    def __init__(self):
        pass

    def tick(self, entities):
        self.speed += self.accelerate / Const.FPS
        self.position += self.speed / Const.FPS
        self.center = self.position
        if not pg.Rect(0, 0, Const.ARENA_SIZE[0], Const.ARENA_SIZE[1]).contains(self):
            self.dead = True

    def touch(self, player):
        return self.player_id != player.player_id and self.colliderect(player)
    
    def activate(self):
        self.dead = True

    def is_dead(self):
        return self.dead

class coffee(throw):
    def __init__(self, player_id, position, direction):
        pg.Rect.__init__(self, 0, 0, Const.COFFEE_WIDTH, Const.COFFEE_HEIGHT)
        self.center = pg.Vector2(position)
        self.position = pg.Vector2(position)
        self.entity_type = Const.COFFEE_TYPE
        self.player_id = player_id
        self.speed = pg.Vector2(Const.COFFEE_SPEED[direction])
        self.accelerate = Const.COFFEE_ACCELERATE * pg.Vector2(0, 1)
        self.damage = Const.COFFEE_DAMAGE
        self.dead = False

class bug(throw):
    def __init__(self, player_id, position, direction):
        pg.Rect.__init__(self, 0, 0, Const.BUG_WIDTH, Const.BUG_HEIGHT)
        self.center = pg.Vector2(position)
        self.position = pg.Vector2(position)
        self.entity_type = Const.BUG_TYPE
        self.player_id = player_id
        self.speed = pg.Vector2(Const.BUG_SPEED[direction])
        self.accelerate = Const.BUG_ACCELERATE * pg.Vector2(0, 1)
        self.damage = Const.BUG_DAMAGE
        self.dead = False
