from AI.team_controller import AI_DIR
import pygame as pg
import Const
from Model.GameObject.basic_game_object import *

AI_DIR_LEFT              = 0
AI_DIR_RIGHT             = 1
AI_DIR_JUMP              = 2
AI_DIR_LEFT_JUMP         = 3
AI_DIR_RIGHT_JUMP        = 4
AI_DIR_ATTACK            = 5
AI_DIR_SPECIAL_ATTACK    = 6

class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.player_id = index

    #常數：player_id: int

    #獲取遊戲資訊專區
    def get_time_left_time(self):
        return self.model.timer // Const.FPS

    def get_game_arena_boundary(self):
        return ((0,0), Const.ARENA_SIZE)
    
    #獲取個人資訊專區
    def get_self_id(self):
        return self.player_id

    def get_self_position(self):
        return tuple(self.model.players[self.player_id].position)
    
    def get_self_speed(self):
        return tuple(self.model.players[self.player_id].speed)

    def get_self_blood(self):
        return self.model.players[self.player_id].blood
    
    def get_keep_item_type(self):
        return self.model.players[self.player_id].keep_item_type

    def get_self_face(self):
        return tuple(self.model.players[self.player_id].face)
    
    def get_self_death(self):
        return self.model.players[self.player_id].death

    def get_self_score(self):
        return self.model.players[self.player_id].score

    def get_can_be_common_attacked(self):
        return self.model.players[self.player_id].can_be_common_attacked()

    def get_can_be_special_attacked(self):
        return self.model.players[self.player_id].can_be_special_attacked()
    
    def get_is_invisible(self):
        return self.model.players[self.player_id].is_invisible()

    def get_can_use_special_attack(self):
        return self.model.players[self.player_id].special_attack_timer == 0 and self.model.players[self.player_id].can_special_attack()
    
    def get_can_jump(self):
        return self.model.players[self.player_id].jump_count < self.model.players[self.player_id].max_jump

    def get_is_jumping(self):
        return self.model.players[self.player_id].speed.y < 0

    def get_infection(self):
        return self.model.players[self.player_id].infection()

    def get_in_folder(self):
        return self.model.players[self.player_id].in_folder()

    def get_damage_adjust(self):
        return self.model.players[self.player_id].damage_adjust()
    
    def get_can_common_attack(self):
        return self.model.players[self.player_id].can_common_attack()
    
    

    #獲取所有玩家資訊專區
    def get_all_position(self):
        return [tuple(player.position) for player in self.model.players]

    def get_all_speed(self):
        return [tuple(player.speed) for player in self.model.players]

    def get_all_face(self):
        return [tuple(player.face) for player in self.model.players]

    def get_all_keep_item_type(self):
        return [player.keep_item_type for player in self.model.players]

    def get_all_can_be_common_attacked(self):
        return [player.can_be_common_attacked() for player in self.model.players]

    def get_all_can_be_specail_attacked(self):
        return [player.can_be_special_attacked() for player in self.model.players]

    def get_all_is_invisible(self):
        return [player.is_invisible() for player in self.model.players]

    def get_all_can_special_attack(self):
        return [player.can_special_attack() and player.special_attack_timer == 0 for player in self.model.players]

    def get_all_infection(self):
        return [player.infection() for player in self.model.players]

    def get_all_in_folder(self):
        return [player.in_folder() for player in self.model.players]

    def get_all_damage_adjust(self):
        return [player.damage_adjust() for player in self.model.players]

    def get_all_score(self):
        return [player.score for player in self.model.players]

    def get_all_player_vector(self):
        all_pos = self.get_all_position()
        my_pos = self.get_self_position()
        return [tuple((dest[0]-my_pos[0], dest[1]-my_pos[1])) for dest in all_pos]

    def get_all_player_distance(self):
        all_vec = self.get_all_player_vector()
        def dist_cal(vec):
            return ((vec[0])**2 + (vec[1])**2) ** (1/2)
        return [dist_cal(vect) for vect in all_vec]

    def get_all_special_attack(self):
        return tuple((special_attack.name,\
                    (special_attack.position[0], special_attack.position[1]),\
                    (special_attack.speed[0], special_attack.speed[1])) for special_attack in self.model.attacks)

    def get_if_player_in_attack_range(self):
        attacker = self.model.players[self.player_id]
        attack_range = attacker.common_attack_range
        for player in self.model.players:
            if attacker.player_id != player.player_id and\
                player.can_be_common_attacked() and attack_range.colliderect(player.rect):
                return True
        return False

        

    #獲取特定玩家資訊專區
    def get_other_position(self,index):
        return tuple(self.model.players[index].position)

    def get_other_speed(self,index):
        return tuple(self.model.players[index].speed)
    
    def get_other_face(self,index):
        return tuple(self.model.players[index].face)
    
    def get_other_keep_item(self,index):
        return self.model.players[index].keep_item_type

    def get_other_can_be_common_attack(self,index):
        return self.model.players[index].can_be_common_attacked()

    def get_other_can_be_special_attack(self,index):
        return self.model.players[index].can_be_special_attacked()

    def  get_other_can_special_attack(self,index):
        return self.model.players[index].can_special_attack() and self.model.players[index].special_attack_timer == 0

    def get_other_is_invisible(self,index):
        return self.model.players[index].is_invisible()

    def get_other_infection(self,index):
        return self.model.players[index].infection()
    
    def get_other_in_folder(self,index):
        return self.model.players[index].in_folder()

    def get_other_damage_adjust(self,index):
        return self.model.players[index].damage_adjust()

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
        nearest_player = self.get_nearest_player_id()     
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

    ###新手友善專區
    def jump(self):
        me = self.model.players[self.player_id]
        if me.speed.y >= 0 and me.jump_count < me.max_jump:
            return AI_DIR_JUMP
        return None

    def jump_or_right(self):
        me = self.model.players[self.player_id]
        if me.speed.y >= 0 and me.jump_count < me.max_jump:
            return AI_DIR_JUMP
        return AI_DIR_RIGHT

    def jump_or_left(self):
        me = self.model.players[self.player_id]
        if me.speed.y >= 0 and me.jump_count < me.max_jump:
            return AI_DIR_JUMP
        return AI_DIR_LEFT

    def get_region(self, pos):
        if pos is None:
            return None
        if pos[1] + 15 < Const.GROUND_POSITION[0][1]:
            return 0
        if pos[1] + 15 < Const.GROUND_POSITION[1][1]:
            return 1
        if pos[1] + 15  < Const.GROUND_POSITION[3][1]:
            return 2
        return 3

    def walk_to_specific_position(self,pos):
        me = self.model.players[self.player_id]
        me.walk_to['walking'] = True
        me.walk_to['end'] = pos

    def stop_to_walk(self):
        me = self.model.players[self.player_id]
        me.walk_to['walking'] = False
        
    def walk_to_position(self,pos1,pos2):###pos1: player, pos2: 指定位置
        playerplatform = self.get_region(pos1)
        specificPlatform = self.get_region(pos2)
        me = self.model.players[self.player_id]
        if playerplatform is None or specificPlatform is None:
            return None
        if playerplatform == specificPlatform:
            if me.rect.collidepoint(pos2):
                me.walk_to['walking'] = False
                return None
            if self.get_is_jumping():
                return None
            if pos1[0]>pos2[0]:
                return AI_DIR_LEFT
            elif pos1[0]<pos2[0]:
                return AI_DIR_RIGHT
            return AI_DIR_JUMP
        elif playerplatform < specificPlatform:
            if playerplatform == 1:
                if pos1[0]<=400:
                    return AI_DIR_RIGHT
                elif pos1[0]>=800:
                    return AI_DIR_LEFT
            return AI_DIR_LEFT
        else:
            if pos1[0] <= 820:
                return AI_DIR_RIGHT
            elif pos1[0]>=900:
                return AI_DIR_LEFT
            else:
                return self.jump()
            '''
            if playerplatform == 1:
                if pos1[0] >= 980:
                    return AI_DIR_LEFT
                elif pos1[0] <= 980 and pos1[0]>=800:
                    return self.left_double_jump()
                elif pos1[0] <= 750:
                    return self.right_double_jump()
            elif playerplatform == 2:
                if pos1[0] <= 750:
                    return AI_DIR_RIGHT
                elif pos1[0] >= 750 and pos1[0] <= 1000:
                    return self.right_double_jump()
                elif pos1[0] >= 1000:
                    return self.left_double_jump()
            elif playerplatform == 3:
                if pos1[0] <= 700:
                    return AI_DIR_RIGHT     

                     
                if pos1[0] <= 800:
                    return self.right_double_jump()
                if pos1[0] <= 980:
                    return self.left_double_jump()
                if pos1[1] >= 980:
                    return AI_DIR_LEFT
            '''

    def walk_to_specific_item(self,item):
        if self.get_nearest_specific_item_position(item) is None:
            return False
        self.walk_to_specific_position(self.get_nearest_specific_item_position(item))
        return True
    
    def get_attack_items(self):
        return [(attack.name, tuple(attack.position)) for attack in self.model.attacks]
