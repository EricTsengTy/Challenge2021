from time import sleep

class TeamAI():
    def __init__(self, helper):
        self.helper = helper

        self.player_id = self.helper.get_self_id()
        self.arena_boundary = self.helper.get_game_arena_boundary()

        self.key_dic = {'left':False, 'right':False, 'jump':False, 'attack':False, 'special_attack':False}
        self.position = self.helper.get_self_position()
        self.all_position = self.helper.get_all_position()
        self.all_position.remove(self.all_position[self.player_id])
        self.can_special_attack = self.helper.get_can_use_special_attack()
        self.can_common_attack = self.helper.get_can_common_attack()
        self.keep_item_type = self.helper.get_keep_item_type()
        self.face = self.helper.get_self_face()
        self.route_mode = 0
        self.block_pos = self.eval_block()

    def decide(self):
        self.update_data()
        self.move()
        self.special_attack_decide()
        self.common_attack_decide()
        return self.key_dic 

    def update_data(self):
        # print(self.helper.get_all_special_attack())
        self.key_dic = {'left':False, 'right':False, 'jump':False, 'attack':False, 'special_attack':False}
        self.position = self.helper.get_self_position()
        self.all_position = self.helper.get_all_position()
        self.all_position.remove(self.all_position[self.player_id])
        self.can_special_attack = self.helper.get_can_use_special_attack()
        self.can_common_attack = self.helper.get_can_common_attack()
        self.keep_item_type = self.helper.get_keep_item_type()
        self.face = self.helper.get_self_face()
        self.block_pos = self.eval_block()

    def move(self):
        pass

    def special_attack_decide(self):
        if not self.can_special_attack: return
        if self.keep_item_type in ('', 'FAN'):
            for pos in self.all_position:
                if self.position[1] - pos[1] < 100 and self.position[1] - pos[1] > -10:
                    self.key_dic['special_attack'] = True
                    if self.face == (1, 0) and self.position[0] > pos[0]:
                        self.key_dic['left'] = True
                        self.key_dic['right'] = False
                    elif self.face == (-1, 0) and self.position[0] < pos[0]:
                        self.key_dic['left'] = False
                        self.key_dic['right'] = True
        elif self.keep_item_type in ('DOS', 'DDOS', 'LIGHTNING', 'THROW_BUG'):
            self.key_dic['special_attack'] = True
        elif self.keep_item_type in ('THROW_COFFEE'):
            self.key_dic['special_attack'] = True
            if self.position[0] < self.arena_boundary[1][0] / 2 and self.face == (-1, 0):
                self.key_dic['right'] = True
                self.key_dic['left'] = False
            elif self.position[0] > self.arena_boundary[1][0] / 2 and self.face == (1, 0):
                self.key_dic['right'] = False
                self.key_dic['left'] = True

    def common_attack_decide(self):
        if not self.can_common_attack: return
        self.key_dic['attack'] = True
        left_count = 0
        right_count = 0
        for pos in self.all_position:
            if self.position[1] - pos[1] >= -120 and self.position[1] - pos[1] < 100:
                if self.position[0] - pos[0] <= 0 and self.position[0] - pos[0] >= -110:
                    right_count += 1
                elif self.position[0] - pos[0] >= 0 and self.position[0] - pos[0] <= 110:
                    left_count += 1
        if left_count > right_count and self.face == (1, 0):
            self.key_dic['left'] = True
            self.key_dic['right'] = False
        elif left_count < right_count and self.face == (-1, 0):
            self.key_dic['left'] = False
            self.key_dic['right'] = True

    def eval_block(self):
        return [self.position[0] // 10, self.position[1] // 10]
