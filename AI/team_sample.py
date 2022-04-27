AI_DIR_LEFT              = 0
AI_DIR_RIGHT             = 1
AI_DIR_JUMP              = 2
AI_DIR_LEFT_JUMP         = 3
AI_DIR_RIGHT_JUMP        = 4
AI_DIR_ATTACK            = 5
AI_DIR_SPECIAL_ATTACK    = 6

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
class TeamAI ():
    def __init__ (self, helper):
        self.helper = helper
        self.enhancement = [0,0,0,0]
    
    def decide (self):
        decision = None        
        if decision is None:
            decision = self.attack()
        if decision is None:
            if self.goto():
                return None
        if decision is None:
            if self.takeOtherItem():
                return None
        if decision is None:
            self.challenge()
            return None
        return decision

    def attack(self):
        if self.helper.get_self_is_jumping():
            return None
        if self.helper.get_self_can_use_special_attack():
            if self.helper.get_self_keep_item_type() == 'DDOS' or self.helper.get_self_keep_item_type()=='DOS':
                return AI_DIR_SPECIAL_ATTACK
            if self.helper.get_region(self.helper.get_self_position()) == self.helper.get_region(self.helper.get_nearest_player_position()):
                return AI_DIR_SPECIAL_ATTACK
        elif self.helper.get_if_any_player_in_attack_range() and self.helper.get_self_can_use_common_attack():
            return AI_DIR_ATTACK
        return None
        ###return self.helper.walk_to_specific_position(self.helper.get_self_position(),self.helper.get_nearest_specific_item_position('EXE'))

    def goto(self):
        if self.helper.get_nearest_specific_item_position('EXE') is not None:
            self.helper.walk_to_position(self.helper.get_nearest_specific_item_position('EXE'))
            return True
        return False
        

    def takeOtherItem(self):
        target = None
        if target is None:
            target = self.helper.walk_to_specific_item('CHARGE')
        if target is None:
            target = self.helper.walk_to_specific_item('DDOS')
        if target is None:
            target = self.helper.walk_to_specific_item('LIGHTNING')
        return target
        
        '''
        if self.helper.get_nearest_specific_item_position('CHARGE') is not None and self.helper.get_region(self.helper.get_self_position()) == self.helper.get_region(self.helper.get_nearest_specific_item_position('CHARGE')):
            return self.helper.walk_to_specific_position(self.helper.get_nearest_specific_item_position('CHARGE'))
        if self.helper.get_nearest_specific_item_position('DOS') is not None and self.helper.get_region(self.helper.get_self_position()) == self.helper.get_region(self.helper.get_nearest_specific_item_position('DOS')):
            return self.helper.walk_to_specific_position(self.helper.get_nearest_specific_item_position('DOS'))
        if self.helper.get_nearest_specific_item_position('DDOS') is not None and self.helper.get_region(self.helper.get_self_position()) == self.helper.get_region(self.helper.get_nearest_specific_item_position('DDOS')):
            return self.helper.walk_to_specific_position(self.helper.get_nearest_specific_item_position('DDOS'))
        if self.helper.get_nearest_specific_item_position('FOLDER_UNUSED') is not None and self.helper.get_region(self.helper.get_self_position()) == self.helper.get_region(self.helper.get_nearest_specific_item_position('FOLDER_UNUSED')):
            return self.helper.walk_to_specific_position(self.helper.get_self_position(),self.helper.get_nearest_specific_item_position('FOLDER_UNUSED'))
        '''

    def challenge(self):
        if self.helper.get_highest_score_player() != self.helper.get_self_id():
            self.helper.walk_to_position(self.helper.get_other_position(self.helper.get_highest_score_player()))
        else:
            self.helper.walk_to_position(self.helper.get_nearest_player_position())

