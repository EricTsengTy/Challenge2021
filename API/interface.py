import imp, traceback, signal
import pygame as pg
import Const
from API.helper import Helper
from EventManager.EventManager import *
import Model.Model

AI_dir_none = {'left':False, 'right':False, 'jump':False, 'attack':False, 'special_attack':False}

class Interface(object):
    def __init__(self, ev_manager, model : Model.Model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.model = model
        self.player_AI = {}
        self.is_init_AI = False

    def notify(self, event: BaseEvent):
        """
        Receive events posted to the message queue.
        """
        if isinstance(event, EventEveryTick):
            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_PLAY:
                self.API_play()
        elif isinstance(event, EventQuit):
            pass
        elif isinstance(event, EventInitialize):
            self.initialize()


    def API_play(self):
        for player in self.model.players:
            if player.is_AI:
                AI_dir = None
                try:
                    AI_dir = self.player_AI[player.player_id].decide()
                except:
                    pass

                if AI_dir == None or AI_dir == AI_dir_none:
                    if player.walk_to['walking']:
                        AI_dir = self.player_AI[player.player_id].helper.how_to_walk(player.walk_to['end'])
                if not isinstance(AI_dir, dict):
                    temp = AI_dir
                    AI_dir = {'left':False, 'right':False, 'jump':False, 'attack':False, 'special_attack':False}
                    if temp == 0:
                        AI_dir['left'] = True
                    elif temp == 1:
                        AI_dir['right'] = True
                    elif temp == 2:
                        AI_dir['jump'] = True
                    elif temp == 3:
                        AI_dir['left'] = True
                        AI_dir['jump'] = True
                    elif temp == 4:
                        AI_dir['right'] = True
                        AI_dir['jump'] = True
                    elif temp == 5:
                        AI_dir['attack'] = True
                    elif temp == 6:
                        AI_dir['special_attack'] = True

                if AI_dir['left']:
                    self.ev_manager.post(EventPlayerMove(player.player_id, 'left'))
                if AI_dir['right']:
                    self.ev_manager.post(EventPlayerMove(player.player_id, 'right'))
                if AI_dir['jump']:
                     self.ev_manager.post(EventPlayerMove(player.player_id, 'jump'))
                if AI_dir['attack']:
                    self.ev_manager.post(EventPlayerAttack(player.player_id))
                if AI_dir['special_attack']:
                    self.ev_manager.post(EventPlayerSpecialAttack(player.player_id))

    def initialize(self):
        if self.is_init_AI:
            return
        self.is_init_AI = True

        for player in self.model.players:
            if player.player_name == "manual":
                continue
            
            # load TeamAI .py file
            # TODO: change the path
            try:
                loadtmp = imp.load_source('', f"./AI/team_{player.player_name}.py")
            except:
                self.load_msg(str(player.player_id), player.player_name, "AI can't load")
                player.player_name, player.is_AI = "Error", False
                continue
            self.load_msg(str(player.player_id), player.player_name, "Loading")
            
            # init TeamAI class
            try:
                self.player_AI[player.player_id] = loadtmp.TeamAI(Helper(self.model, player.player_id))
            except:
                self.load_msg(str(player.player_id), player.player_name, "AI init crashed")
                traceback.print_exc()
                player.player_name, player.is_AI = "Error", False
                continue
            try:
                player.enhance(self.player_AI[player.player_id].enhancement)
            except:
                pass
            self.load_msg(str(player.player_id), player.player_name, "Successful to Load")

    def load_msg(self, player_id, player_name ,msg):
        print(f"[{str(player_id)}] team_{player_name}.py: {msg}")
