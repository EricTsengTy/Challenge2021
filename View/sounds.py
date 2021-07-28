import pygame as pg
import os.path
import Const
from EventManager.EventManager import *
from Model.Model import GameEngine


class Audio():
    sound_list = {
        #'attack; = pg.mixer.Sound(os.path.join(Const.SOUND.PATH, 'attack.wav'))
        'attack':None,
        'jump':None,
        'fireball':None,
    }
    
    def __init__(self, ev_manager: EventManager, model: GameEngine):
        self.ev_manager = ev_manager
        self.model = model
        ev_manager.register_listener(self)

    def notify(self, event):
        if isinstance(event, EventPlayerAttack):
            self.sound_list['attack'].play()
    