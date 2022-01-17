import Const
from math import sqrt

class attacker():
    def __init__(self, AI):
        self.AI = AI
        self.helper = AI.helper
        self.eps = 0.01
        self.radius = 300
        self.id = self.helper.get_self_id()
        self.sp_delay = Const.PLAYER_SPECIAL_ATTACK_DELAY / Const.FPS
        self.thre = {'' : 0.25,
                     'FAN' : 0.1, 
                     'LIGHTNING' : -1, 
                     'THROW_COFFEE' : 0.3,
                     'THROW_BUG' : 0.3,
                     'DOS' : -1,
                     'DDOS' : -1,
                    }
        self.refresh = ['FAN', 'THROW_COFFEE', 'THROW_BUG', 'DOS', 'DDOS', 'LIGHTNING']
        self.pos = self.center(self.helper.get_self_position())
        self.actionset = self.AI.actionset
        self.stored_ability = None

    def update(self):
        self.pos = self.center(self.helper.get_self_position())
        self.actionset = self.AI.actionset ## not sure if nessesary

    def check_melee(self):
        if self.helper.get_if_player_in_attack_range():
            self.actionset['attack'] = True

    def redirect_sp_attack(self):
        if 0 <= self.helper.get_self_special_attack_delay() <= 1:
            tmp, tmp2 = self.ability_land_prob(self.stored_ability, 1), self.ability_land_prob(self.stored_ability, -1)
            if tmp > tmp2 + self.eps:
                self.actionset['right'] = True
                return True
            elif tmp2 > tmp + self.eps:
                self.actionset['left'] = True
                return True
        return False

    def check_going_to_get_item():
        if self.helper.get_can_use_special_attack():
            for item in self.refresh:
                pos_list = self.helper.get_all_specific_item_position(item)
                for pos in pos_list:
                    if self.dist(self.center_item(pos), self.center(self.pos)) < self.radius:
                        self.actionset['special_attack'] = True
                        self.stored_ability = self.helper.get_keep_item_type()

    def check_sp_attack(self):
        if self.helper.get_can_use_special_attack():
            my_item = self.helper.get_keep_item_type()
            if self.ability_land_prob(my_item) > self.thre[my_item]:
                self.actionset['special_attack'] = True
                self.stored_ability = my_item

    def center(self, pos):
        return (pos[0] + Const.PLAYER_WIDTH / 2, pos[1] + Const.PLAYER_HEIGHT / 2)

    def dist(self, xx, yy):
        return sqrt((xx[0] - yy[0]) ** 2 + (xx[1] - yy[1]) ** 2)

    def ability_land_prob(self, ability, face = None):
        tmp_pos = self.helper.get_all_position()
        cbs = self.helper.get_all_can_be_special_attacked()
        tmp_speed = self.helper.get_all_speed()
        pos = []
        phantom = [] # not used yet
        for i in range(4):
            if i != self.id and cbs[i]:
                pos.append(self.center(tmp_pos[i]))
                phantom.append(self.center((tmp_pos[i][0] + tmp_speed[i][0] * self.sp_delay\
                    , tmp_pos[i][1] + tmp_speed[i][1] * self.sp_delay)))
        if len(pos) == 0:
            return 0.
        land_prob = 0.
        def rangetest(pp, factor):
            if face == None: 
                return max(0, 1 - abs(pp[0] - self.pos[0]) / factor)
            else:
                if (pp[0] - self.pos[0]) * face >= 0:
                    return max(0, 1 - (pp[0] - self.pos[0]) / factor)
                else: 
                    return 0

        if ability == '':
            for p in pos:
                land_prob += max(0, 1 - abs(p[1] - self.pos[1]) / 200)\
                     * rangetest(p, 1600)
        elif ability == 'FAN':
            for p in pos:
                land_prob += max(0, 1 - abs(p[1] - self.pos[1]) / 450) * rangetest(p, 1600)  
        elif ability == 'LIGHTNING':
            for p in pos:
                if p[1] < self.pos[1] + 50:
                    land_prob += rangetest(p, 200)     
        elif ability == 'THROW_COFFEE':
            for p in pos:
                if p[1] < self.pos[1] + 50:
                    land_prob += 0.5 + 0.5 * rangetest(p, 500)
        elif ability == 'THROW_BUG':
            for p in pos:
                land_prob += min(1, 500 / max(1, self.dist(p, self.pos)))
        else:
            return 0
        return land_prob