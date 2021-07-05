import pygame as pg
import Const

def init():
    state = {
                'special_attack':0,
                'be_common_attacked':0,
                'be_special_attacked':0,
                'in_folder':0,
                'infected':0,
                'slow_move_speed':0,
                'fast_special_attack_speed':0,
                'invisible':0,
                'immune':0
            }
    return state

def normal(state):
    state = {
                'special_attack':0,
                'be_common_attacked':0,
                'be_special_attacked':0,
                'in_folder':0,
                'infected':0,
                'slow_move_speed':0,
                'fast_special_attack_speed':0,
                'invisible':0,
                'immune':0
            }

def infect(state):
    if state['immune'] != 0:
        return
    state['infected'] = 3 * Const.FPS #Const.INFECTED_TIME
    state['special_attack'] = 3 * Const.FPS #Const.INFECTED_TIME

def invisible(state):
    state['invisible'] = int(0.5*Const.FPS) #Const.INVISIBLE_TIME
    state['be_common_attacked'] = int(0.5*Const.FPS) #Const.INVISIBLE_TIME
    state['be_special_attacked'] = int(0.5*Const.FPS) #Const.INVISIBLE_TIME

def folder(state):
    state['in_folder'] = 3 * Const.FPS #Const.IN_FOLDER_TIME
    state['special_attack'] = 3 * Const.FPS #Const.IN_FOLDER_TIME
    state['be_common_attacked'] = 3 * Const.FPS #Const.IN_FOLDER_TIME
    state['be_special_attacked'] = 3 * Const.FPS #Const.IN_FOLDER_TIME

def slow_down(state):
    state['slow_move_speed'] = 3 * Const.FPS #Const.SLOW_DOWN_TIME

def broken(state):
    state['special_attack'] = 3 * Const.FPS #Const.BROKEN_TIME

def firewall(state):
    state['immune'] = 3 * Const.FPS #Const.FIREWALL_TIME

def graphiccard(state):
    state['fast_special_attack_speed'] = 3 * Const.FPS #Const.GRAPHIC_CARD_TIME


