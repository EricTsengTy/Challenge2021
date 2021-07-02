import random
import pygame as pg
from pygame.sprite import collide_mask
import Const
from pygame.math import Vector2
from EventManager.EventManager import *
from Model.GameObject.player import Player
from Model.GameObject.ground import Ground
from Model.GameObject.item import *

class StateMachine(object):
    '''
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.

    TL;DR. Just for game state recording.
    '''
    def __init__(self):
        self.statestack = []

    def peek(self):
        '''
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        '''
        try:
            return self.statestack[-1]
        except IndexError:
            # empty stack
            return None

    def pop(self):
        '''
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        '''
        try:
            return self.statestack.pop()
        except IndexError:
            # empty stack
            return None

    def push(self, state):
        '''
        Push a new state onto the stack.
        Returns the pushed value.
        '''
        self.statestack.append(state)
        return state

    def clear(self):
        '''
        Clear the stack.
        '''
        self.statestack = []


class GameEngine:
    '''
    The main game engine. The main loop of the game is in GameEngine.run()
    '''

    def __init__(self, ev_manager: EventManager):
        '''
        This function is called when the GameEngine is created.
        For more specific objects related to a game instance
            , they should be initialized in GameEngine.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.state_machine = StateMachine()

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        self.clock = pg.time.Clock()
        self.state_machine.push(Const.STATE_MENU)
        self.players = [Player(self, i) for i in range(Const.PLAYER_NUMBER)]
        self.grounds = [Ground(self, i[0], i[1], i[2], i[3]) for i in Const.GROUND_POSITION]
        self.items = []

    def notify(self, event: BaseEvent):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            # Peek the state of the game and do corresponding work
            cur_state = self.state_machine.peek()
            if cur_state == Const.STATE_MENU:
                self.update_menu()

            elif cur_state == Const.STATE_PLAY:
                self.update_objects()
                self.timer -= 1
                if self.timer == 0:
                    self.ev_manager.post(EventTimesUp())

            elif cur_state == Const.STATE_ENDGAME:
                self.update_endgame()

        elif isinstance(event, EventStateChange):
            if event.state == Const.STATE_POP:
                if self.state_machine.pop() is None:
                    self.ev_manager.post(EventQuit())
            else:
                self.state_machine.push(event.state)

        elif isinstance(event, EventQuit):
            self.running = False

        elif isinstance(event, EventPlayerMove):
            # player move left / move right / jump
            self.players[event.player_id].move(event.direction)

        elif isinstance(event, EventPlayerAttack):
            # player do common attack
            attacker = event.player_id[0]
            if self.players[attacker].can_common_attack:
                attack_range = self.players[attacker].common_attack_range
                for i in range(Const.PLAYER_NUMBER):
                    if i == attacker:
                        continue
                    if self.players[i].can_be_common_attacked() and attack_range.colliderect(self.players[i]):
                        self.players[i].be_common_attacked()
            
        elif isinstance(event, EventTimesUp):
            self.state_machine.push(Const.STATE_ENDGAME)

    def update_menu(self):
        '''
        Update the objects in welcome scene.
        For example: game title, hint text
        '''
        pass

    def update_objects(self):
        '''
        Update the objects not controlled by user.
        For example: obstacles, items, special effects
        '''
        for player in self.players:
            player.tick()
        for item in self.items:
            item.tick()
        
        for player in self.players:
            player.check_touch_item()
        
        
        # # player is invisible
        # for player in self.players:
        #     if player.is_invisible:
        #         player.invisible_time -= 1
        #         if player.invisible_time == 0:
        #             player.is_invisible = False

        #remove item
        for item in list(self.items): # iterating the copy of original list
            if item.is_dead():
                if item.item_type == 'FOLDER_UNUSED':
                    new_item = Item(item.left, item.top, 'FOLDER_USED')
                    new_item.activate()
                    self.items.append(new_item)
                self.items.remove(item)

        # generate the items
        while len(self.items) < 5:
            if random.random() < 0.8:
                self.items.append(Item(self,
                                       random.randint(0, Const.ARENA_SIZE[0] - Const.ITEM_WIDTH),
                                       random.randint(300, 400),'FOLDER_USED'))

    def update_endgame(self):
        '''
        Update the objects in endgame scene.
        For example: scoreboard
        '''
        pass

    def run(self):
        '''
        The main loop of the game is in this function.
        This function activates the GameEngine.
        '''
        self.running = True
        # Tell every one to start
        self.ev_manager.post(EventInitialize())
        self.timer = Const.GAME_LENGTH
        while self.running:
            self.ev_manager.post(EventEveryTick())
            self.clock.tick(Const.FPS)
