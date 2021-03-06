import random
from typing import Tuple
import pygame as pg
from pygame.sprite import collide_mask
import Const
from pygame.math import Vector2
from EventManager.EventManager import *
from Model.GameObject.player import Player
from Model.GameObject.ground import Ground
from Model.GameObject.item import *
from Model.GameObject.item_generator import *
import Model.GameObject.state as State
from Model.GameObject.color_selector import *

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

    def __init__(self, ev_manager: EventManager, AI_names: list):
        '''
        This function is called when the GameEngine is created.
        For more specific objects related to a game instance
            , they should be initialized in GameEngine.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.state_machine = StateMachine()

        self.AI_names = AI_names
        while len(self.AI_names) < 4:
            self.AI_names.append('m')

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        self.clock = pg.time.Clock()
        self.timer = Const.GAME_LENGTH
        self.state_machine.push(Const.STATE_MENU)
        self.players = [Player(self, i, 'manual', False) if self.AI_names[i] == 'm' else Player(self, i, self.AI_names[i], True) for i in range(Const.PLAYER_NUMBER)]
        self.grounds = [Ground(self, i[0], i[1], i[2], i[3]) for i in Const.GROUND_POSITION]
        self.items = []
        self.attacks = []
        self.item_generator = Item_Generator(self)
        self.color_selector = Color_Selector(self.players)
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
                    for player in self.players:
                        if player.death == 0:
                            player.add_score(Const.SCORE_NEVER_DIE)
                    self.ev_manager.post(EventTimesUp())

            elif cur_state == Const.STATE_STOP:
                return

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
            if self.players[event.player_id].in_folder():
                return
            self.players[event.player_id].move(event.direction)

        elif isinstance(event, EventPlayerAttack):

           # player do common attack
            attacker = self.players[event.player_id]
            if attacker.can_common_attack(): 
                self.ev_manager.post(EventNormalAttackMovement(event.player_id))
                attack_range = attacker.common_attack_range
                for player in self.players:
                    if attacker.player_id != player.player_id and\
                       player.can_be_common_attacked() and attack_range.colliderect(player.rect):
                        player.be_common_attacked(attacker)
                attacker.common_attack_timer = Const.PLAYER_COMMON_ATTACK_TIMER
    
        elif isinstance(event, EventPlayerSpecialAttack):

            attacker = self.players[event.player_id]
            if attacker.can_special_attack():
                attacker.special_attack()

        elif isinstance(event, EventPreviousColor):
            self.color_selector.previous_color(self.players[event.player_id])

        elif isinstance(event, EventNextColor):
            self.color_selector.next_color(self.players[event.player_id])
            
        elif isinstance(event, EventTimesUp):
            self.state_machine.push(Const.STATE_ENDGAME)

        elif isinstance(event, EventRestart):
            self.initialize()

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
        self.item_generator.tick()

        for player in list(self.players):
            if player.killed(): self.players.remove(player)
            else: player.tick()
        
        for item in (self.items):
            if item.killed(): self.items.remove(item)
            else: item.tick()
        
        for attack in list(self.attacks):
            if attack.killed(): self.attacks.remove(attack)
            else: attack.tick()

    def update_endgame(self):
        '''
        Update the objects in endgame scene.
        For example: scoreboard
        '''

    def run(self):
        '''
        The main loop of the game is in this function.
        This function activates the GameEngine.
        '''
        self.running = True
        # Tell every one to start
        self.ev_manager.post(EventInitialize())
        while self.running:
            self.ev_manager.post(EventEveryTick())
            self.clock.tick(Const.FPS)
