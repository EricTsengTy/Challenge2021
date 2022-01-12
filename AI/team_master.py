'''
ITEM_TYPE_LIST=['FAN' : directed,
                'LIGHTNING' : directed,
                'THROW_COFFEE' : directed AOE,
                'THROW_BUG' : AOE,
                'DOS' : targeted & very good,
                'DDOS' : targeted & good,
                'EXE' : instant & very good,
                'USB' : useless,
                'FIREWALL' : instant & good,
                'GRAPHIC_CARD' : instant & normal,
                'FORMAT' : useless,
                'FOLDER_UNUSED' : useless,
                'CHARGE' : useless
                ]
'''
import Const
from math import sqrt

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.default_actionset = {'left' : False, 'right' : False, 'jump' : False, 'attack' : False, 'special_attack' : False}
        self.actionset = self.default_actionset
        self.id = self.helper.get_self_id()
        # self.pos = self.helper.get_self.position()
        self.sp_delay = Const.PLAYER_SPECIAL_ATTACK_DELAY / Const.FPS
        self.thre = {'' : 0.3 * 2,
                     'FAN' : 0.5 * 2, 
                     'LIGHTNING' : -1, 
                     'THROW_COFFEE' : 0.7,
                     'THROW_BUG' : 0.8,
                     'DOS' : -1,
                     'DDOS' : -1,
                    }
        self.stored_ability = None
        self.eps = 0.01
        self.pos = self.center(self.helper.get_self_position())

    def decide(self):
        self.actionset = self.default_actionset
        self.pos = self.center(self.helper.get_self_position())
        # if auto attack can hit, land the hit
        self.check_melee()
        # if directed ability's land probability is good, do it
        self.check_sp_attack()
        # try redirect directed ability if needed
        self.redirect_sp_attack()
        # find the nearest useful item, and go to it
        # if "is going to get a new item", use current item
        #print(self.actionset)
        return self.actionset

    def check_melee(self):
        if self.helper.get_if_player_in_attack_range():
            self.actionset['attack'] = True

    def check_sp_attack(self):
        if self.helper.get_can_use_special_attack():
            my_item = self.helper.get_keep_item_type()
            # print(self.ability_land_prob(my_item))
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
                return max(0, 1 - abs(pp[0] - self.pos[0]))
            else:
                if (pp[0] - self.pos[0]) * face >= 0:
                    return max(0, 1 - (pp[0] - self.pos[0]) / factor)
                else: 
                    return 0

        if ability == '':
            for p in pos:
                land_prob += max(0, 1 - abs(p[1] - self.pos[1]) / 200)\
                     * rangetest(p, 1000)
        elif ability == 'FAN':
            for p in pos:
                land_prob += max(0, 1 - abs(p[1] - self.pos[1]) / 400)\
                     * rangetest(p, 1000)  
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
                land_prob += min(1, 1.5 * rangetest(p, 300))
        else:
            return 0
        return land_prob

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





