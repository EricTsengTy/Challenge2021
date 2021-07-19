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
        return

    def get_nearest_specific_item_position(self,item_id):
        return

    def get_all_item_position(self,item_id):
        return

    def get_all_specific_item_postion(self,item_id):
        return

    #獲取特別資訊專區
    def get_nearest_player_id(self):
        return
    
    def get_nearest_player_position(self):
        return

    def get_highest_score_player(self):
        return

    def get_distance(self):
        return

    def get_vector(self,pos1, pos2):
        return