from AI.libmaster.pathfinder_v2 import pathfinder
from AI.libmaster.attacker import attacker
import Const

class TeamAI():
    def __init__(self, helper):
        self.item_value = {
            'FAN'          : (1.0, 130),
            'LIGHTNING'    : (0.1,-250),
            'THROW_COFFEE' : (1.0, 130),
            'THROW_BUG'    : (1.3, 300),
            'DOS'          : (1.1, 200),
            'DDOS'         : (2.5, 500),
            'EXE'          : (2.2, 400),
            'USB'          : (0.1,-250),
            'FIREWALL'     : (1.1, 200),
            'GRAPHIC_CARD' : (0.5,-250),
            'FORMAT'       : (0.1,-250),
            'FOLDER_UNUSED': (0.1,-250),
            'CHARGE'       : (0.2,-250)
        }
        self.helper = helper
        self.default_actionset = {'left' : False, 'right' : False, 'jump' : False, 'attack' : False, 'special_attack' : False}
        self.actionset = self.default_actionset.copy()

        self.attacker = attacker(self)
        self.pathfinder = pathfinder(self, item_value = self.item_value)

        self.time = 0
        self.pos = self.helper.get_self_position()

    def feet(self):
        return (self.pos[0] + Const.PLAYER_WIDTH / 2, self.pos[1] + Const.PLAYER_HEIGHT)

    def item_center(self, pos):
        return (pos[0] + Const.ITEM_HEIGHT / 2, pos[1] + Const.ITEM_WIDTH / 2)

    def decide(self):
        # update info
        self.pos = self.helper.get_self_position()
        self.actionset = self.default_actionset.copy()
        self.attacker.update()
        # if auto attack can hit, land the hit
        self.attacker.check_melee()
        # if directed ability's land probability is good, do it
        self.attacker.check_sp_attack()
        # try redirect directed ability if needed
        # print("attacker done")
        if not self.attacker.redirect_sp_attack():
            # pathfinder
            self.pathfinder.update()
            self.pathfinder.move()
        # print("done")
        return self.actionset
