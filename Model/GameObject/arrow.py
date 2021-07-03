import pygame as pg
import Const
import random
from Model.GameObject.basic_game_object import Basic_Game_Object


class Arrow(Basic_Game_Object):
	def __init__(self, model, attacker_id, position, direction, damage):
		super().__init__(model, position.x, position.y, 1, 1)
		self.name = 'Arrow'
		self.attacker_id = attacker_id
		self.speed = direction.normalize() * Const.ARROW_SPEED
		self.damage = damage
		self.dead = False

	def tick(self):
		self.basic_tick()
		for player in self.model.players:
			if self.attacker_id != player.player_id\
				and player.rect.collidepoint(self.center.x, self.center.y):
				player.be_special_attacked(self)
				self.kill()
