import pygame as pg
import Const
import random
from Model.GameObject.basic_game_object import Basic_Game_Object


class Arrow(Basic_Game_Object):
	def __init__(self, model, player_id, position, direction, damage):
		super().__init__(model, position.x, position.y, 1, 1)
		self.player_id = player_id
		self.speed = direction.normalize() * Const.ARROW_SPEED
		self.damage = damage
		self.dead = False

	def tick(self, entities):
		self.basic_tick()
		if not pg.Rect(0, 0, Const.ARENA_SIZE[0], Const.ARENA_SIZE[1]).collidepoint(self.position.x, self.position.y):
			self.dead = True
    
    def touch(self, player):
		return self.player_id != player.player_id and player.would_be_special_attacked() and player.collidepoint(self.position.x, self.position.y)

    def activate(self):
    	return
        self.dead = True

	def is_dead(self):
		return self.dead