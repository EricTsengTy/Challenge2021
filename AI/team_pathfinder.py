from AI.libmaster.pathfinder_v2 import pathfinder
import Const

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0,0,0,0]
        self.default_actionset = {'left' : False, 'right' : False, 'jump' : False, 'attack' : False, 'special_attack' : False}
        self.actionset = self.default_actionset.copy()
        self.pathfinder = pathfinder(self)
        self.pos = (0, 0)

    def feet(self):
        return (self.pos[0] + Const.PLAYER_WIDTH / 2, self.pos[1] + Const.PLAYER_HEIGHT)

    def item_center(self, pos):
        return (pos[0] + Const.ITEM_HEIGHT / 2, pos[1] + Const.ITEM_WIDTH / 2)

    def decide(self):
        self.pos = self.helper.get_self_position()
        #print(self.feet())
        
        tar = self.helper.get_nearest_item_position()
        self.actionset = self.default_actionset.copy()
        if tar is not None:
            print("working...")
            speed = self.helper.get_self_speed()[1]
            jmp = self.helper.get_self_remaining_jumps()
            # print("jmp = ", jmp)
            d, action = self.pathfinder.find(self.feet(), self.item_center(tar), speed, jmp)
            if action is not None:
                print(action)
                if action[0] > 0:
                    self.actionset['right'] = True
                elif action[0] < 0:
                    self.actionset['left'] = True
                if action[1] > 0:
                    self.actionset['jump'] = True
        print("done")
        return self.actionset
        
        

