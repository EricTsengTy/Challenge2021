AI_DIR_LEFT              = 0
AI_DIR_RIGHT             = 1
AI_DIR_JUMP              = 2
AI_DIR_LEFT_JUMP         = 3
AI_DIR_RIGHT_JUMP        = 4
AI_DIR_ATTACK            = 5
AI_DIR_SPECIAL_ATTACK    = 6

class TeamAI():
    def __init__ (self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0, 0]
    
    def decide (self):
        # use special attack
        if self.helper.get_self_can_use_special_attack():
            return AI_DIR_SPECIAL_ATTACK
        # pick the nearest item
        pos = self.helper.get_nearest_item_position()
        if pos is not None:
            self.helper.walk_to_position(pos)
        return None
