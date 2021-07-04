import pygame as pg
import Const
from math import sqrt

# create a "lightning"
class Lightning():
	'''
	special attack: lightning
	discription: create lightnings around the caster, which expands quickly throughout the 8 directions.
				 damaging each player hit
	lightning can only damage the same player once
	the hitbox detection is a (8) line
	'''
	def __init__(self, caster): 
		self.pos = pg.Vector2(caster.x + Const.CENTER_OFFSET_X, caster.y + Const.CENTER_OFFSET_Y)
		self.speed = Const.SPELL_LIGHTNING_SPEED / Const.FPS
		self.damage = Const.SPELL_LIGHTNING_DAMAGE
		self.range = Const.SPELL_LIGHTNING_INIT_RANGE
		self.timer = Const.SPELL_LIGHTNING_TIME
		self.immune = [False for _ in range(Const.PLAYER_NUMBER)]
		self.immune[caster.player_id] = True
		self.n = Const.PLAYER_NUMBER
		self.directions = (pg.Vector2(1, 0), pg.Vector2(sqrt(2)/2, sqrt(2)/2), pg.Vector2(0, 1), pg.Vector2(sqrt(2)/2, -sqrt(2)/2))

	def draw_lines(self, d):
		'''
		d: 0 to 3
		return: two pg.vec2, indicating the two endpoint of the line along that direction
		'''
		return (self.pos + self.directions[d] * self.range, self.pos - self.directions[d] * self.range)

	def update(self, players): 
		'''
		Input: the players
		Output: a tuple, ((a, b, c, d), x)
		(a, b, c, d) indicates the damage dealt to player 0, 1, 2, 3, respectively
		x = True/False indicates whether this object should be deleted
		'''
		self.timer -= 1
		damage = [0 for _ in range(self.n)]
		for i in range(3):
			line = self.draw_lines(i)
			for player in players:
				if (not self.immune[player.player_id]) and (not damage[player.player_id]) and players[i].clipline(line):
					damage[player.player_id] = damage

		return (damage, self.timer == 0)

