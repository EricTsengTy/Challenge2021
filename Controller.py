import pygame as pg

from EventManager import *
from Model import GameEngine
import Const


class Controller:
    '''
    Handles the control input. Either from keyboard or from AI.
    '''

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        '''
        This function is called when the Controller is created.
        For more specific objects related to a game instance
            , they should be initialized in Controller.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.model = model

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        pass

    def notify(self, event: BaseEvent):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            key_down_events = []
            # Called once per game tick. We check our keyboard presses here.
            for event_pg in pg.event.get():
                # handle window manager closing our window
                if event_pg.type == pg.QUIT:
                    self.ev_manager.post(EventQuit())
                if event_pg.type == pg.KEYDOWN:
                    key_down_events.append(event_pg)

            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU: self.ctrl_menu(key_down_events)
            if cur_state == Const.STATE_PLAY: self.ctrl_play(key_down_events)
            if cur_state == Const.STATE_STOP: self.ctrl_stop(key_down_events)
            if cur_state == Const.STATE_ENDGAME: self.ctrl_endgame(key_down_events)

    def ctrl_menu(self, key_down_events):
        for event_pg in key_down_events:
            if event_pg.type == pg.KEYDOWN and event_pg.key == pg.K_SPACE:
                self.ev_manager.post(EventStateChange(Const.STATE_PLAY))

    def ctrl_play(self, key_down_events):
        # handle movement using key pressed state
        keys = pg.key.get_pressed()
        for k, v in Const.PLAYER_MOVE_KEYS.items():
            if keys[k]:
                self.ev_manager.post(EventPlayerMove(*v))
        
        for event_pg in key_down_events:
            # handle attack using keydown events
            if event_pg.type == pg.KEYDOWN:
                key = event_pg.key
                if key in Const.PLAYER_ATTACK_KEYS:
                    player_id = Const.PLAYER_ATTACK_KEYS[key]
                    self.ev_manager.post(EventPlayerAttack(player_id))
                if key in Const.PLAYER_SPECIAL_ATTACK_KEYS:
                    player_id = Const.PLAYER_SPECIAL_ATTACK_KEYS[key]
                    self.ev_manager.post(EventPlayerSpecialAttack(player_id))
                # detect stop
                if event_pg.key == Const.GAME_STOP_KEY:
                    self.ev_manager.post(EventStop())


    def ctrl_stop(self, key_down_events):
        # detect start/stop events
        for event_pg in key_down_events:
            if event_pg.key == Const.GAME_CONTINUE_KEY:
                self.ev_manager.post(EventContinue())

    def ctrl_endgame(self, key_down_events):
        # detect restart event
        for event_pg in key_down_events:
            if event_pg.key == Const.GAME_RESTART_KEY:
                self.ev_manager.post(EventRestart())