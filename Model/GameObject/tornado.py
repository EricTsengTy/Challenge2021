import pygame as pg
import Const

# create a "tornado"
class Tornado(pg.Rect):
	'''
	special attack: tornado
	discription: the caster launchs a tornado in the faced direction, damaging every enemy player hit.
	the tornado can only damage the same player once
	the hitbox detection is a "rectangle"
	'''
	def __init__(self, caster, direction):
        pg.Rect.__init__(self, (caster.x + Const.PLAYER_WIDTH, caster.y + Const.PLAYER_HEIGHT - Const.SPELL_TORNADO_HEIGHT, Const.SPELL_TORNADO_WIDTH, Const.SPELL_TORNADO_HEIGHT))
		self.pos = [caster.x + Const.CENTER_OFFSET_X, caster.y + Const.CENTER_OFFSET_Y]
		self.speed = Const.SPELL_TORNADO_SPEED * direction / Const.FPS
		self.damage = Const.SPELL_TORNADO_DAMAGE
		self.immune = [False for _ in range(Const.PLAYER_NUMBER)]
		self.immune[caster.player_id] = True
		self.n = Const.PLAYER_NUMBER
		self.arena = Const.ARENA_SIZE

	def update(self, players): 
		'''
		Input: the players
		Output: a tuple, ((a, b, c, d), x)
		(a, b, c, d) indicates the damage dealt to player 0, 1, 2, 3, respectively
		x = True/False indicates whether this object should be deleted
		'''
		destroy = False
		damage = [0 for _ in range(self.n)]

		# damage calculation
		for player in players:
			if (not self.immune[player.player_id]) and self.colliderect(player):
				damage[player.player_id] = self.damage

		# move the fireball
		self.pos[0] += self.speed
		if self.pos[0] > Const.ARENA_SIZE or self.pos[0] < 0:
			destroy = True

		return (damage, destroy)