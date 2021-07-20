import pygame as pg
import Const
from Model.GameObject.basic_game_object import *

AI_DIR_LEFT        = 0
AI_DIR_RIGHT       = 1
AI_DIR_JUMP        = 2
AI_DIR_ATTACK      = 3
AI_DIR_USE_ITEM    = 4

class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.player_id = index

    #常數：player_id: int

    #獲取遊戲資訊專區
    def get_time_left_time(self):
        return 

    def get_game_arena_boundary(self):
        return 

    #獲取個人資訊專區
    def get_self_id(self):
        return

    def get_self_position(self):
        return 
    
    def get_self_velocity(self):
        return 

    def get_self_blood(self):
        return
    
    def get_keep_item_type(self):
        return

    def get_self_direction(self):
        return 
    
    def get_self_death(self):
        return

    def get_self_score(self):
        return

    def get_can_be_common_attack(self):
        return

    def get_can_be_special_attack(self):
        return
    
    def get_is_vincible(self):
        return

    def get_can_special_attack(self):
        return
    
    def get_can_jump(self):
        return

    def get_infection(self):
        return

    def get_in_folder(self):
        return

    def get_damage_adjust(self):
        return

    #獲取所有玩家資訊專區
    def get_all_position(self):
        return

    def get_all_velocity(self):
        return

    def get_all_direction(self):
        return

    def get_all_keep_item_type(self):
        return

    def get_all_can_be_common_attack(self):
        return

    def get_all_can_be_specail_attack(self):
        return 

    def get_all_is_invisible(self):
        return

    def get_all_can_special_attack(self):
        return

    def get_all_infection(self):
        return

    def get_all_in_folder(self):
        return

    def get_all_damage_adjust(self):
        return

    def get_all_score(self):
        return

    def get_all_player_vector(self):
        return

    def get_all_player_distance(self):
        return


    #獲取特定玩家資訊專區
    def get_other_position(self,index):
        return

    def get_other_velocity(slef,index):
        return
    
    def get_other_direction(self,index):
        return

    def get_other_normal_speed(self,index):
        return

    def get_other_jump_speed(self,index):
        return
        
    def get_other_keep_item(self,index):
        return

    def get_other_can_be_common_attack(self,index):
        return

    def get_other_can_be_special_attack(self,index):
        return

    def  get_other_can_special_attack(self,index):
        return

    def get_other_is_invisible(self,index):
        return

    def get_other_infection(self,index):
        return
    
    def get_other_in_folder(self,index):
        return

    def get_other_damage_adjust(self,index):
        return

    #獲取道具資訊專區

    def get_nearest_item_position(self):
        nearest_pos, minimum_distance = None, 10000
        for item in self.model.items:
            distance = self.get_distance(self.get_self_position(), item.position)
            if distance < minimum_distance:
                minimum_distance, nearest_pos = distance, tuple(item.position)
        return nearest_pos

    def get_nearest_specific_item_position(self, items_type):
        nearest_pos, minimum_distance = None , 10000
        specific_items = [item for item in self.model.items if item.item_type == items_type]
        for item in specific_items:
            distance = self.get_distance(self.get_self_position(), item.position)
            if distance < minimum_distance:
                minimum_distance, nearest_pos = distance , tuple(item.position)
        return nearest_pos

    def get_all_item_position(self):
        return [tuple(item.position) for item in self.model.items]

    def get_all_specific_item_postion(self, items_type):
        return [tuple(item.position) for item in self.model.items if item.item_type == items_type]

    #獲取特別資訊專區
    def get_nearest_player_id(self):
        index, minimum_distance = None, 10000
        for player in self.model.players:
            distance = self.get_distance(self.get_self_position(), player.position)
            if player.player_id != self.player_id  and distance < minimum_distance:
                minimum_distance, index = distance, player.player_id
        return index
    
    def get_nearest_player_position(self):
        nearest_player = self.get_nearest_player()     
        return self.get_other_position(nearest_player)     


    def get_highest_score_player(self):
        index, highest_score = None, -1
        for player in self.model.players:
            if player.player_id != self.player_id and player.score > highest_score:
                highest_score, index = player.score, player.player_id
        return index

    def get_distance(self, pos1, pos2):
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def get_vector(self, pos1, pos2):
        return (pos2[0] - pos1[0], pos2[1] - pos1[1])