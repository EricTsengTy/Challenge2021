import random
import pygame as pg
from pygame.sprite import collide_mask
import Const
from pygame.math import Vector2
from EventManager.EventManager import *
from Model.GameObject.player import Player
from Model.GameObject.block import Block
from Model.GameObject.item import *
from Model.GameObject.arrow import *
from Model.GameObject.throw import *

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
        self.players = [Player(i) for i in range(Const.PLAYER_NUMBER)]
        self.blocks = [Block(i[0], i[1], i[2], i[3]) for i in Const.BLOCK_POSITION]
        self.items = []
        self.entities = []

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
            if self.players[event.player_id].can_move():
                self.players[event.player_id].move(event.direction)

        elif isinstance(event, EventPlayerAttack):
            # player do common attack
            attacker = event.player_id[0]
            if self.players[attacker].can_common_attack():
                attack_range = self.players[attacker].common_attack_range
                for i in range(Const.PLAYER_NUMBER):
                    if i == attacker:
                        continue
                    if self.players[i].would_be_common_attacked() and attack_range.colliderect(self.players[i]):
                        self.players[i].be_common_attacked(Const.PLAYER_COMMON_ATTACK_DAMAGE * self.players[i].multiple_of_damage())

        elif isinstance(event, EventPlayerSpecialAttack):
            attacker = self.players[event.player_id[0]]
            if attacker.can_special_attack():
                if attacker.keep_item_type == Const.COFFEE_TYPE:
                    self.entities.append(coffee(attacker.player_id, attacker.position, "left"))
                elif attacker.keep_item_type == Const.BUG_TYPE:
                    self.entities.append(bug(attacker.player_id, attacker.position, "left"))
                elif attacker.keep_item_type == Const.DOS_TYPE:
                    be_attacked = [_ for _ in self.players]
                    be_attacked.remove(attacker)
                    be_attacked = random.choice(be_attacked)
                    self.entities.append(dos(attacker.player_id, attacker.position, be_attacked.position - attacker.position)) 
                elif attacker.keep_item_type == Const.DDOS_TYPE:
                    be_attacked = [_ for _ in self.players]
                    be_attacked.remove(attacker)
                    be_attacked = random.choice(be_attacked)
                    self.entities.append(ddos(attacker.player_id, be_attacked.position)) 
                    
                attacker.keep_item_type = 0

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
        # player fall
        for player in self.players:
            player.move_every_tick()
        
        # player touch the ground (landing)
        for player in self.players:
            collided = player.collidelist(self.blocks)
            collided = self.blocks[collided] if collided!=-1 else None
            if player.vertical_speed>0 and collided!=None and collided.bottom>player.bottom>collided.top:
                player.bottom = collided.top
                player.vertical_speed = 0
                player.jump_count = 0
                player.sync(last_modify='rect')
        
        # player state
        for player in self.players:
            player.states_tick()

        # player touch the item
        for item in self.items:
            player_touched = item.collidelist(self.players)
            player_touched = self.players[player_touched] if player_touched!=-1 else None
            if player_touched != None:
                player_touched.touch_item(item.item_type)
                item.activate()

        for item in self.items:
            item.tick()

        #remove item
        removed_item=[]
        for item in self.items:
            if item.is_dead():
                if item.item_type == Const.FOLDER_UNUSED_TYPE:
                    new_item = Item(item.left,
                                    item.top,
                                    Const.FOLDER_USED_TYPE)
                    new_item.activate()
                    self.items.append(new_item)
                removed_item.append(item)
        for item in removed_item:
            self.items.remove(item)
            
        # generate the items
        while len(self.items) < 5:
            if random.random() < 0.8:
                self.items.append(Item(random.randint(0, Const.ARENA_SIZE[0] - Const.ITEM_WIDTH),
                                    random.randint(350, 400),
                                    Const.BUG_TYPE))

        #entity move every tick
        for entity in self.entities:
            entity.tick(self.entities)

        #player touch entity
        for player in self.players:
            for entity in self.entities:
                if entity.touch(player):
                    entity.activate()

        #remove entity
        remove_entity = []
        for entity in self.entities:
            if entity.is_dead():
                remove_entity.append(entity)
        for entity in remove_entity:
            self.entities.remove(entity)

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
