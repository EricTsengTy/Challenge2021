import pygame as pg
import os.path
import Const
from EventManager.EventManager import *
from Model.Model import GameEngine
from View import SOUND_ENABLE

if(SOUND_ENABLE):
    class Audio():
        sound_list = {
            'attack': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'attack.wav')),
            'jump':None,
            'fireball':pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'fireball.wav')),
            'lightning':pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'lightning.wav')),
            'tornado': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'fan.wav')),
            'get_prop': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'pick_up.wav')),
        }
        
        def __init__(self, ev_manager: EventManager, model: GameEngine):
            self.ev_manager = ev_manager
            self.model = model
            ev_manager.register_listener(self)

            self.sound_list['get_prop'].set_volume(0.5)
            self.sound_list['lightning'].set_volume(0.7)

        def notify(self, event):
            if isinstance(event, EventPlayerAttack):
                self.sound_list['attack'].play()
            if isinstance(event, EventSpecialAttackMovement):
                if event.attack_type == '':
                    self.sound_list['fireball'].play()
                if event.attack_type == 'LIGHTNING':
                    self.sound_list['lightning'].play()
                if event.attack_type == 'FAN':
                    self.sound_list['tornado'].play()
            if isinstance(event, EventGetProp):
                self.sound_list['get_prop'].play()
else:
    class Audio():
        def __init__(self, ev_manager: EventManager, model: GameEngine):
            pass

        def notify(self, event):
            pass