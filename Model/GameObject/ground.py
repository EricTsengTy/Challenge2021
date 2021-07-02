from Model.GameObject.basic_game_object import Basic_Game_Object
import pygame as pg

class Ground(Basic_Game_Object):
    def __init__(self, model, left, top, width, height):
        super().__init__(model, left, top, width, height) 
