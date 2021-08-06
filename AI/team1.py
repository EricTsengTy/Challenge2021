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
class TeamAI ():
    def __init__ (self, helper):
        self.helper = helper
    
    def decide (self):

        decision = None

        if decision is None:
            decision = self.attack()
        if decision is None:
            decision = self.goto()    
        if decision is None:
            decision = self.special()
        if decision is None:
            decision = self.can()
        return decision

    def attack():
        pass

    def goto():
        pass

    def special():
        pass

    def can():
        pass


