AI_DIR_LEFT              = 0
AI_DIR_RIGHT             = 1
AI_DIR_JUMP              = 2
AI_DIR_LEFT_JUMP         = 3
AI_DIR_RIGHT_JUMP        = 4
AI_DIR_DOUBLE_JUMP       = 5
AI_DIR_ATTACK            = 6
AI_DIR_SPECIAL_ATTACK    = 7



'''
FAN,
LIGHTNING,
THROW_COFFEE,
THROW_BUG,
DOS,
DDOS,
EXE,
USB,
FIREWALL,
GRAPHIC_CARD,
FORMAT,
FOLDER_UNUSED,
CHARGE 
'''

AI_DIR = {'left': False, 'right': False, 'jump': False, 'attack': False, 'special_attack': False}   
class TeamAI ():
    def __init__ (self, helper):
        self.helper = helper

    def decide (self):
        for dir in AI_DIR:
            AI_DIR[dir] = False   
        self.special_attack()
        self.attack()
        #self.walk_to_EXE()
        #self.walk_to_nearest_player() # if no walk_to_EXE
        return AI_DIR
        '''
        decision = None
        if decision is None:
            decision = self.special_attack()
        if decision is None:
            decision = self.walk_to_EXE()    
        if decision is None:
            decision = self.attack()
        if decision is None:
            decision = self.walk_to_nearest_player()
        return decision
        '''

    def special_attack(self):
        if self.helper.get_can_use_special_attack() :
            AI_DIR['special_attack'] = True

    def attack(self):
        if self.helper.get_can_common_attack() and self.helper.get_if_player_in_attack_range():
            AI_DIR['attack'] = True

    def walk_to_EXE(self):
    
        if self.helper.get_nearest_specific_item_position("EXE") == None:
            return None
        ###if self.helper.get_keep_item_type() != "" and  self.helper.get_can_use_special_attack() == True:
        ###    return AI_DIR_ATTACK
        nearest_player = self.helper.get_nearest_player_position()
        nearest_EXE = self.helper.get_nearest_specific_item_position("EXE")
        if self.helper.get_distance(self.helper.get_self_position(),nearest_player) < self.helper.get_distance(self.helper.get_self_position(),nearest_EXE):
            return self.helper.walk_to_specific_position(nearest_EXE)
        
        if self.helper.get_can_be_common_attacked() == True or self.helper.get_can_be_special_attacked():
            return None
        return self.helper.walk_to_specific_position(nearest_EXE)

        ''' tonpon version
        nearest_EXE = self.helper.get_nearest_specific_item_position("EXE")
        if nearest_EXE == None:
            return None
        return self.helper.walk_to_specific_position(nearest_EXE)
        '''



    def walk_to_nearest_player(self):
        pos_y = self.helper.get_self_position()[1]
        nearest_y = self.helper.get_nearest_player_position()[1]
        if pos_y == nearest_y or pos_y < nearest_y:
            if self.helper.get_vector(self.helper.get_self_position(),self.helper.get_nearest_player_position())[0] > 0:
                return AI_DIR_RIGHT
            else:
                return AI_DIR_LEFT
        else:
            if self.helper.get_self_position()[0]<=0:
                return AI_DIR_RIGHT_JUMP
            elif self.helper.get_self_position()[0] >= self.helper.get_game_arena_boundary()[1][0]:
                return AI_DIR_LEFT_JUMP
            if abs(self.helper.get_vector(self.helper.get_self_position(),self.helper.get_nearest_player_position())[0]) <= 100:
                return AI_DIR_DOUBLE_JUMP
            elif self.helper.get_vector(self.helper.get_self_position(),self.helper.get_nearest_player_position())[0] > 0:
                return AI_DIR_RIGHT_JUMP
            else:
                return AI_DIR_LEFT_JUMP
           

