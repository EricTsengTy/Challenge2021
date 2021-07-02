import pygame as pg
import Const

class States:
    def __init__(self):
        self.in_the_state = False
        self.remain_time = 0

    def into(self,time):
        self.in_the_state = True
        self.remain_time = time * Const.FPS

    def tick(self):
        self.remain_time -= 1
        if self.remain_time == 0:
            self.in_the_state = False

class StatesList:
    def __init__(self):
        self.can_not_special_attack = States()
        self.get_virus = States()
        self.be_infective = States()
        self.use_firewall = States()
        self.run_slowly = States()
        self.be_in_folder = States()
        self.be_invisible = States()
        self.use_video_card = States()
        self.states = [self.can_not_special_attack, self.get_virus, self.be_infective, self.use_firewall, self.run_slowly, self.be_in_folder, self.be_invisible, self.use_video_card]

    def can_special_attack(self):
        return (not self.can_not_special_attack.in_the_state) and (not self.get_virus.in_the_state) and (not self.be_in_folder.in_the_state)
    
    def can_common_attack(self):
        return (not self.be_in_folder.in_the_state)

    def would_be_special_attacked(self):
        return (not self.use_firewall.in_the_state) and (not self.be_in_folder.in_the_state) and (not self.be_invisible.in_the_state)
    
    def would_be_common_attacked(self):
        return (not self.be_in_folder.in_the_state) and (not self.be_invisible.in_the_state)

    # multiple of common attack damage
    def multiple_of_damage(self):
        if self.get_virus.in_the_state:
            return Const.DAMAGE_MULTIPLE
        return 1

    def can_infect(self):
        return self.be_infective.in_the_state

    def would_be_infected(self):
        return (not self.use_firewall.in_the_state)

    def multiple_of_speed(self):
        if self.run_slowly.in_the_state:
            return Const.SPEED_MULTIPLE
        return 1

    def can_move(self):
        return (not self.be_in_folder.in_the_state)

    # multiple of special attack energy
    def multiple_of_energy(self):
        if self.use_video_card.in_the_state:
            return Const.ENERGY_MULTIPLE
        return 1

    def states_tick(self):
        for state in self.states:
            if state.in_the_state:
                state.tick()

    def states_clean(self):
        for state in self.states:
            state.in_the_state = False
            state.remain_time = 0
