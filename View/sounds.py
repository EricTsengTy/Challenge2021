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
            'get_prop': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'pick_up.wav')),
            'lightning':pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'lightning.wav')),
            'tornado': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'fan.wav')),
            'dos': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'dos.wav')),
            'ddos': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'ddos.wav')),
            'charge': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'charge.wav')),
            'throw_coffee': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'throw_coffee.wav')),
            'throw_bug': pg.mixer.Sound(os.path.join(Const.SOUND_PATH, 'throw_bug.wav'))
        }
        
        def __init__(self, ev_manager: EventManager, model: GameEngine):
            self.ev_manager = ev_manager
            self.model = model
            ev_manager.register_listener(self)

            self.sound_list['get_prop'].set_volume(0.5)
            self.sound_list['lightning'].set_volume(0.7)
            self.sound_list['dos'].set_volume(0.4)
            self.sound_list['ddos'].set_volume(0.4)
            self.sound_list['charge'].set_volume(0.5)
            self.sound_list['throw_coffee'].set_volume(0.5)
            self.sound_list['throw_bug'].set_volume(0.7)

        def notify(self, event):
            if isinstance(event, EventPlayerAttack):
                self.sound_list['attack'].play()
            elif isinstance(event, EventSpecialAttackMovement):
                if event.attack_type == '':
                    self.sound_list['fireball'].play()
                elif event.attack_type == 'LIGHTNING':
                    self.sound_list['lightning'].play()
                elif event.attack_type == 'FAN':
                    self.sound_list['tornado'].play()
                elif event.attack_type == 'DOS':
                    self.sound_list['dos'].play()
                elif event.attack_type == 'DDOS':
                    self.sound_list['ddos'].play()
                elif event.attack_type == 'THROW_COFFEE':
                    self.sound_list['throw_coffee'].play()
                elif event.attack_type == 'THROW_BUG':
                    self.sound_list['throw_bug'].play()
                

            elif isinstance(event, EventGetProp):
                self.sound_list['get_prop'].play()
                
                if event.item_type == 'CHARGE':
                    self.sound_list['charge'].play()
            
            elif isinstance(event, EventHelloWorld):
                #print(event.style)
                pass
else:
    class Audio():
        def __init__(self, ev_manager: EventManager, model: GameEngine):
            pass

        def notify(self, event):
            pass