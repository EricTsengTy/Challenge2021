AI_DIR_LEFT              = 0
AI_DIR_RIGHT             = 1
AI_DIR_JUMP              = 2
AI_DIR_LEFT_JUMP         = 3
AI_DIR_RIGHT_JUMP        = 4
AI_DIR_ATTACK            = 5
AI_DIR_SPECIAL_ATTACK    = 6

FIREBALL_HEIGHT = 50

class TeamAI ():
    def __init__ (self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0, 0]
        self.ID = self.helper.get_self_id()
        self.pos = None
        self.action = None
        self.timer = 0
        
    def decide (self):
        if self.timer == 0:
            self.action, self.timer = self.decide_dodge()
            if self.action is None and self.helper.get_self_can_use_common_attack():
                self.action, self.timer = self.decide_common_attack()
            if self.action is None and self.helper.get_self_can_use_special_attack():
                self.action, self.timer = self.decide_special_attack()
            if self.action is None:
                self.action, self.timer = self.decide_pick_item()
        self.timer -= 1
        return self.action

    def decide_dodge(self):
        """
        Dodge special attacks. Sorted by importance.
        """
        self.pos = self.helper.get_self_position()     
        # ddos
        ddoss = self.helper.get_ddos()
        for ddos in ddoss:
            ddos_center = ddos[1]
            if self.helper.get_distance(self.pos, ddos_center) < 200:
                return AI_DIR_LEFT if self.pos[0] > 600 else AI_DIR_RIGHT, 180
        for special_attack in self.helper.get_all_special_attack():
            if special_attack[1] == self.ID:
                continue
            name, pos, vel = special_attack[0], special_attack[2], special_attack[3]
            # fireball
            if name == "Fireball":
                distance = self.helper.get_distance(pos, self.pos)
                if pos[1] >= self.pos[1] - FIREBALL_HEIGHT and distance < 250:
                    return AI_DIR_JUMP, 1
        return None, 1
    
    def decide_common_attack(self):
        if self.helper.get_if_any_player_in_attack_range():
            return AI_DIR_ATTACK, 1
        return None, 1

    def decide_special_attack(self):
        if self.helper.get_self_keep_item_type() != "":
            return AI_DIR_SPECIAL_ATTACK, 1
        return None, 1
    
    def decide_pick_item(self):
        pos = self.helper.get_nearest_item_position()
        if pos is not None:
            self.helper.walk_to_position(pos)
        return None, 1
