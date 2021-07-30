AI_DIR_LEFT              = 0
AI_DIR_RIGHT             = 1
AI_DIR_JUMP              = 2
AI_DIR_LEFT_JUMP         = 3
AI_DIR_RIGHT_JUMP        = 4
AI_DIR_DOUBLE_JUMP       = 5
AI_DIR_ATTACK            = 6
AI_DIR_SPECIAL_ATTACK    = 7

'''
'':NO_ITEM (default:fireball)
BANANA_PISTOL 
BIG_BLACK_HOLE 
CANCER_BOMB 
ZAP_ZAP_ZAP 
BANANA_PEEL 
RAINBOW_GROUNDER 
INVINCIBLE_BATTERY 
'''

class TeamAI ():
    def __init__ (self, helper):
        self.helper = helper

    def decide (self):
        decision = None
        if decision is None:
            decision = self.special_attack()
        if decision is None:
            decision = self.walk_to_EXE()    
        if decision is None:
            decision = self.attack()
        if decision is None:
            decision = self.walk_to_nearest_player()
    
    def special_attack(self):
        pass

    def walk_to_EXE(self):
        pass

    def attack(self):
        pass

    def walk_to_nearest_player(self):
        pass
