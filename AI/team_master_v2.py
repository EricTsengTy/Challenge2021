import Const
from attacker import attacker
from pathfinder_v2 import pathfinder

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.default_actionset = {'left' : False, 'right' : False, 'jump' : False, 'attack' : False, 'special_attack' : False}
        self.actionset = self.default_actionset.copy()

        self.attacker = attacker(self)
        self.pathfinder = pathfinder(self)

        self.time = 0

    def decide(self):
        # update info
        self.actionset = self.default_actionset.copy()
        self.attacker.update()
        # if auto attack can hit, land the hit
        self.attacker.check_melee()
        # if directed ability's land probability is good, do it
        self.attacker.check_sp_attack()
        # try redirect directed ability if needed
        if not self.attacker.redirect_sp_attack():
            # pathfinder
            self.pathfinder.update()
            self.pathfinder.move() 
        print("done")
        return self.actionset
    '''
    def check_melee(self):
        if self.attacker.check_melee():
            self.actionset['attack'] = True

    def self.check_sp_attack(self):
        if self.attacker.check_sp_attack():
            self.actionset['special_attack'] = True

    def redirect_sp_attack(self):
        return self.attacker.redirect_sp_attack(self.actionset)

    def move(self):
        self.pathfinder.move(self.actionset)
    '''

