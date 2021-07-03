import pygame as pg
import Const
from pygame.math import Vector2
from Model.GameObject.basic_game_object import Basic_Game_Object

class Dos(Basic_Game_Object):
	def __init__(self, player):
		super().__init__(player.model, player.position.x, player.position.y, 1, 1)
		self.timer = Const.DOS_TIMER
		self.rounds = Const.DOS_ACTIVE_LIMIT

	entities.append(arrow(player.model, player.id, player.position, direction, damage))
