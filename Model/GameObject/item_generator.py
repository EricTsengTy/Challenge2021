import pygame as pg
import Const
import random
from Model.GameObject.item import *
from Model.GameObject.basic_game_object import Basic_Game_Object

class Item_Generator:
    def __init__(self, model):
        self.model = model
        self.generate_cd = 0

    def generate_a_item(self):
        while True:
            px = random.randint(0, Const.ARENA_SIZE[0] - Const.ITEM_WIDTH)
            py = random.randint(0, Const.ARENA_SIZE[1] - Const.ITEM_HEIGHT - 70 )
            generate_item = Item(self.model, px, py, random.choice(Const.ITEM_TYPE_LIST))
            collided = False
            for item in self.model.items:
                if(generate_item.rect.colliderect(item.rect)):
                    collided = True
                    break
            for player in self.model.players:
                if(generate_item.rect.colliderect(player.rect)):
                    collided = True
                    break
            if not collided:
                self.model.items.append(generate_item)
                return

    def tick(self):
        self.generate_cd -= 1
        if self.generate_cd<=0:
            while len(self.model.items) < Const.MAX_ITEM_NUMBER:
                self.generate_a_item()
            self.generate_cd = Const.ITEM_GENERATOR_COOLDOWN
