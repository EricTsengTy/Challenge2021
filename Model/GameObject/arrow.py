import pygame as pg
import Const
import random
from Model.GameObject.basic_game_object import Basic_Game_Object


class Arrow(Basic_Game_Object):
	def __init__(self, model, player_id, position, direction, damage):
		super().__init__(model, position.x, position.y, 1, 1)
		self.name = 'Arrow'
		self.player_id = player_id
		self.speed = direction.normalize() * Const.ARROW_SPEED
		self.damage = damage
		self.dead = False

	def tick(self):
		self.basic_tick()
    
	def touch(self, player):
		return self.player_id != player.player_id and player.would_be_special_attacked() and player.collidepoint(self.position.x, self.position.y)

	def activate(self):
		return
		self.dead = True

	def is_dead(self):
		return self.dead