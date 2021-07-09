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
    state['infection'] = max(Const.INFECTED_TIME,state['infection'])
    state['special_attack'] = max(Const.INFECTED_TIME,state['special_attack'])
    state['infected_common_attack'] = max(Const.INFECTED_COMMON_ATTACK_TIME,state['infected_common_attack'])

def invisible(state):
    state['invisible'] = max(Const.INVISIBLE_TIME, state['invisible'])
    state['be_common_attacked'] = max(Const.INVISIBLE_TIME, state['be_common_attacked'])
    state['be_special_attacked'] = max(Const.INVISIBLE_TIME, state['be_special_attacked'])

def folder(state):
    state['in_folder'] = max(Const.IN_FOLDER_TIME, state['in_folder'])
    state['special_attack'] = max(Const.IN_FOLDER_TIME, state['special_attack'])
    state['be_common_attacked'] = max(Const.IN_FOLDER_TIME, state['be_common_attacked'])
    state['be_special_attacked'] = max(Const.IN_FOLDER_TIME, state['be_special_attacked'])

def slow_down(state):
    state['slow_move_speed'] = max(Const.SLOW_DOWN_TIME, state['slow_move_speed'])

def broken(state, time):
    state['special_attack'] = max(time, state['special_attack'])

def firewall(state):
    state['immune'] = max(Const.FIREWALL_TIME, state['immune'])

def graphiccard(state):
    state['fast_special_attack_speed'] = max(Const.GRAPHIC_CARD_TIME, state['fast_special_attack_speed'])
