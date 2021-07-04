import pygame as pg

from EventManager.EventManager import *
from Model.Model import GameEngine
import Const
import View.staticobjects
from View.utils import Text


class GraphicalView:
    '''
    Draws the state of GameEngine onto the screen.
    '''
    background = pg.Surface(Const.ARENA_SIZE)

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        '''
        This function is called when the GraphicalView is created.
        For more specific objects related to a game instance
            , they should be initialized in GraphicalView.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.model = model

        self.screen = pg.display.set_mode(Const.WINDOW_SIZE)
        pg.display.set_caption(Const.WINDOW_CAPTION)
        self.background.fill(Const.BACKGROUND_COLOR)

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        pg.init()
        pg.font.init()
        pg.display.set_caption(Const.WINDOW_CAPTION)
        
        # static objects
        self.players = View.staticobjects.View_players(self.model)

    def notify(self, event):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            self.display_fps()

            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU: self.render_menu()
            elif cur_state == Const.STATE_PLAY: self.render_play()
            elif cur_state == Const.STATE_STOP: self.render_stop()
            elif cur_state == Const.STATE_ENDGAME: self.render_endgame()

    def display_fps(self):
        '''
        Display the current fps on the window caption.
        '''
        pg.display.set_caption(f'{Const.WINDOW_CAPTION} - FPS: {self.model.clock.get_fps():.2f}')

    def render_menu(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # draw text

        '''
        font = pg.font.Font(None, 36)
        text_surface = font.render("Press [space] to start ...", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))
        '''
        menu_text = Text("Press [space] to start ...", 36, pg.Color('gray88'))
        menu_text.blit(self.screen, center=(Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2))

        pg.display.flip()

    def render_play(self, target=None, update=True):
        if target is None:
            target = self.screen
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)
        
        # draw players
        self.players.draw(target)

        for block in Const.BLOCK_POSITION:
            pg.draw.rect(self.screen, Const.BLOCK_COLOR, pg.Rect(*block))
        
        for item in self.model.items:
            pg.draw.rect(self.screen, Const.ITEM_COLOR, item)
        
        for entity in self.model.entities:
            if entity.entity_type == Const.ARROW_TYPE:
                pg.draw.circle(self.screen, Const.ARROW_COLOR, entity.position, Const.ARROW_RADIUS)
            elif entity.entity_type == Const.COFFEE_TYPE:
                pg.draw.rect(self.screen, Const.COFFEE_COLOR, entity)
            elif entity.entity_type == Const.BUG_TYPE:
                pg.draw.rect(self.screen, Const.BUG_COLOR, entity)
        pg.display.flip()

    def render_stop(self):
        pass

    def render_endgame(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        pg.display.flip()
