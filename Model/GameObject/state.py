import pygame as pg
import Const

def init():
    state = {
                'infected_common_attack':0,
                'special_attack':0,
                'be_common_attacked':0,
                'be_special_attacked':0,
                'in_folder':0,
                'infection':0,
                'slow_move_speed':0,
                'fast_special_attack_speed':0,
                'invisible':0,
                'immune':0
            }
    return state

def infect(state):
    if state['immune'] != 0:
        return
    state['infection'] = Const.INFECTED_TIME
    state['special_attack'] = Const.INFECTED_TIME
    state['infected_common_attack'] = Const.INFECTED_COMMON_ATTACK_TIME

def invisible(state):
    state['invisible'] = Const.INVISIBLE_TIME
    state['be_common_attacked'] = Const.INVISIBLE_TIME
    state['be_special_attacked'] = Const.INVISIBLE_TIME

def folder(state):
    state['in_folder'] = Const.IN_FOLDER_TIME
    state['special_attack'] = Const.IN_FOLDER_TIME
    state['be_common_attacked'] = Const.IN_FOLDER_TIME
    state['be_special_attacked'] = Const.IN_FOLDER_TIME

def slow_down(state):
    state['slow_move_speed'] = Const.SLOW_DOWN_TIME

def broken(state, time):
    state['special_attack'] = time

def firewall(state):
    state['immune'] = Const.FIREWALL_TIME

def graphiccard(state):
    state['fast_special_attack_speed'] = Const.GRAPHIC_CARD_TIME


