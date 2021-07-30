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
