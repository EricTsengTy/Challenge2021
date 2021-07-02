import pygame as pg
import Const

# create a "fireball"
class Fireball():
	'''
	special attack: fireball
	discription: fires a fireball, starts from the center of the caster, moving horizonally, 
				 damaging every enemy player hit.
	the fireball can only damage the same player once
	the hitbox detection is a "ball"
	'''
	def __init__(self, caster, direction): # direction = +1 : +x
		self.pos = [caster.x + Const.CENTER_OFFSET_X, caster.y + Const.CENTER_OFFSET_Y]
		self.speed = Const.SPELL_FIREBALL_SPEED * direction / Const.FPS
		self.radius = Const.SPELL_FIREBALL_RADIUS
		self.damage = Const.SPELL_FIREBALL_DAMAGE
		self.immune = [False for _ in range(Const.PLAYER_NUMBER)]
		self.immune[caster.player_id] = True
		self.n = Const.PLAYER_NUMBER
		self.arena = Const.ARENA_SIZE
		# self.life # destroy upon hitting the edge

	def check_col(self, recta): # check if a rectangle collide with a ball (self)
		rxl = recta.x
		rxr = rxl + Const.PLAYER_WIDTH
		ryu = recta.y
		ryb = ryu + Const.PLAYER_HEIGHT
		tmpx = -1
		tmpy = -1
		if self.pos[0] > rxr:
			tmpx = 1
		elif self.pos[0] > rxl:
			tmpx = 0
		if self.pos[1] > ryb:
			tmpy = 1
		elif self.pos[1] > ryu:
			tmpy = 0
		if tmpx == 0:
			if tmpy == 1:
				return self.pos[1] - ryb < self.radius
			elif tmpy == -1:
				return ryu - self.pos[1] < self.radius
			else: # 0
				return True
		if tmpy == 0:
			if tmpx == 1:
				return self.pos[0] - rxr < self.radius
			elif tmpx == -1:
				return rxl - self.pos[0] < self.radius
		corx = rxl if tmpx == -1 else rxr
		cory = ryu if tmpy == -1 else rxl
		return (self.pos[0] - corx) ** 2 + (self.pos[1] - cory) ** 2 < self.radius ** 2

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
			if (not self.immune[player.player_id]) and self.check_col(player):
				damage[player.player_id] = self.damage

		# move the fireball
		self.pos[0] += self.speed
		if self.pos[0] > Const.ARENA_SIZE or self.pos[0] < 0:
			destroy = True

		return (damage, destroy)




