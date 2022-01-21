import pygame as pg

from EventManager.EventManager import *
from Model.Model import GameEngine
import Const
import View.staticobjects
import View.activeobjects
import View.animation
import View.players
import random


class GraphicalView:
    '''
    Draws the state of GameEngine onto the screen.
    '''
    background = pg.Surface(Const.ARENA_SIZE)
    fullscreen = False

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        '''
        This function is called when the GraphicalView is created.
        For more specific objects related to a game instance
            , they should be initialized in GraphicalView.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.model = model
        self.is_initialized = False

    def _create_screen(self, fullscreen=False):
        try:
            self.screen = pg.display.set_mode(Const.WINDOW_SIZE, (pg.FULLSCREEN if fullscreen else 0) | pg.SCALED)
            self.low_resolution = False
        except pg.error:
            self.low_resolution = True
            self.real_window_size = (Const.WINDOW_SIZE[0] * 2 // 3, Const.WINDOW_SIZE[1] * 2 // 3)
            self.real_screen = pg.display.set_mode(self.real_window_size, (pg.FULLSCREEN if fullscreen else 0) | pg.SCALED)
            self.screen = pg.Surface(Const.WINDOW_SIZE)

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        pg.init()
        pg.font.init()
        pg.display.set_caption(Const.WINDOW_CAPTION)

        if not self.is_initialized:
            self._create_screen(self.fullscreen)

        # animations
        self.animation_list = []

        if not self.is_initialized:
             View.staticobjects.init_staticobjects()
             View.activeobjects.init_activeobjects()
             View.animation.init_animation()
        # static objects
        self.menu =  View.staticobjects.View_menu(self.model)
        self.tutorial = View.staticobjects.View_tutorial(self.model)
        self.stage =  View.staticobjects.View_stage(self.model)
        self.platform = View.staticobjects.View_platform(self.model)
        self.arrow = View.staticobjects.View_Arrow(self.model)
        self.item = View.staticobjects.View_Item(self.model)
        self.pause_window = View.staticobjects.View_Pause(self.model)
        self.scoreboard = View.staticobjects.View_Scoreboard(self.model)
        self.score_playing = View.staticobjects.View_Score_Playing(self.model)
        # active objects
        self.bug = View.activeobjects.View_Bug(10)
        self.coffee = View.activeobjects.View_Coffee(10)
        self.fireball = View.activeobjects.View_Fireball(10)
        self.tornado = View.activeobjects.View_Tornado(10)
        self.lightning = View.activeobjects.View_Lightning(5)
        self.color_select = View.activeobjects.View_ColorPicker(self.model, 7)

        self.is_initialized = True

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
            elif cur_state == Const.STATE_TUTORIAL: self.render_tutorial()
            elif cur_state == Const.STATE_COLOR_SELECT: self.render_color_select()
            elif cur_state == Const.STATE_PLAY: self.render_play()
            elif cur_state == Const.STATE_STOP: self.render_stop()
            elif cur_state == Const.STATE_ENDGAME: self.render_endgame()

            if self.low_resolution:
                self.real_screen.blit(pg.transform.smoothscale(self.screen, self.real_window_size), (0, 0))
                pg.display.flip()

        elif isinstance(event, EventToggleFullScreen):
            self.toggle_fullscreen()

        elif isinstance(event, EventNormalAttackMovement):
            self.players.status[event.player_id] = 'common_attack'
            self.players.timer[event.player_id] = 0

        elif isinstance(event, EventHelloWorld):
            event.style = random.randint(1,3)
            if event.style == 1:
                self.animation_list.append(View.animation.Greeting_from_audience(3,40)) #delay_of_frames, num
            elif event.style == 2:
                self.animation_list.append(View.animation.Greeting_from_prog(0))
            elif event.style == 3:
                self.animation_list.append(View.animation.Greeeting_from_player(self.model))

        elif isinstance(event, EventBeAttacked):
            # event.player_id
            if self.model.players[event.player_id].state['immune'] == 0 and self.players.status[event.player_id] != 'be_attacked':
                self.players.status[event.player_id] = 'be_attacked'
                self.players.timer[event.player_id] = 0

            if self.model.players[event.player_id].state['immune'] != 0:
                self.players.atmosphere[event.player_id]['firewall'] = 1

        elif isinstance(event, EventSpecialAttackMovement):
            # event.player_id
            # event.attack_type
            if event.attack_type == '':
                self.players.status[event.player_id] = f'special_attack_fireball'
            else:
                self.players.status[event.player_id] = f'special_attack_{event.attack_type}'
                #print(f'special_attack_{event.attack_type}')
            self.players.timer[event.player_id] = 0

        elif isinstance(event, EventGetProp):

            if event.item_type == 'CHARGE':
                self.players.atmosphere[event.player_id]['charge'] = 0
            elif event.item_type == 'FIREWALL':
                pass
            elif event.item_type == 'FORMAT':
                self.players.atmosphere[event.player_id]['format'] = 0
            elif event.item_type != 'FOLDER_UNUSED':
                self.players.atmosphere[event.player_id]['get_prop'] = 0

        elif isinstance(event, EventPlayerDie):
            self.players.reset(event.player_id)
        elif isinstance(event, EventStateChange):
            if event.state == Const.STATE_PLAY:
                #players
                self.players = View.players.View_players(self.model, 7)
        elif isinstance(event, EventRestart):
            self.initialize()

    def display_fps(self):
        '''
        Display the current fps on the window caption.
        '''
        pg.display.set_caption(f'{Const.WINDOW_CAPTION} - FPS: {self.model.clock.get_fps():.2f}')

    def render_menu(self, target=None):
        if target is None:
            target = self.screen
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)
        self.menu.draw(target)

        pg.display.flip()

    def render_tutorial(self, target=None):
        if target is None:
            target = self.screen
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)
        self.tutorial.draw(target)
        pg.display.flip()

    def render_color_select(self, target=None):
        '''
        implement color select view here
        '''
        if target is None:
            target = self.screen
        self.screen.fill(Const.BACKGROUND_COLOR)
        self.color_select.draw(target)

        pg.display.flip()

    def render_play(self, target=None, update=True):
        if target is None:
            target = self.screen

        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)
        self.stage.draw(target)
        self.platform.draw(target)
        self.score_playing.draw(target)

        # draw players
        self.players.draw(target)

        for item in self.model.items:
            self.item.draw(self.screen, item.rect, item.item_type)

        for attack in self.model.attacks:
            if attack.name == 'Arrow':
                self.arrow.draw(target, attack.position, attack.speed)
            elif attack.name == 'Bug':
                self.bug.draw(target, attack.position, attack.state_timer, attack.track)
            elif attack.name == 'Coffee':
                self.coffee.draw(target, attack.position, attack.timer, attack.track)
            elif attack.name == 'Fireball':
                self.fireball.draw(target, attack.position, attack.timer, attack.speed)
            elif attack.name == 'Tornado':
                self.tornado.draw(target, attack.rect.center, attack.timer, attack.speed)
            elif attack.name == 'Lightning':
                self.lightning.draw(target, attack.destination, attack.timer, attack.position)

        #animation
        for ani in self.animation_list:
            if ani.expired:
                self.animation_list.remove(ani)
            else:
                ani.draw(target, update)

        pg.display.flip()

    def render_stop(self):
        self.pause_window.draw(self.screen)
        pg.display.flip()

    def render_endgame(self):
        self.scoreboard.draw(self.screen)
        pg.display.flip()


    def toggle_fullscreen(self):
        self.ev_manager.post(EventStop())
        # save screen content before toggling
        old_screen = pg.display.get_surface().copy()
        caption = pg.display.get_caption()
        cursor = pg.mouse.get_cursor()
        w, h = old_screen.get_width(), old_screen.get_height()
        flags = old_screen.get_flags()
        bits = old_screen.get_bitsize()

        pg.display.quit()
        pg.display.init()

        # toggle fullscreen
        self.fullscreen = not self.fullscreen
        self._create_screen(self.fullscreen)

        # restore _screen content
        self.screen.blit(old_screen, (0, 0))
        pg.display.set_caption(*caption)

        pg.key.set_mods(0)
        pg.mouse.set_cursor(*cursor)

        self.ev_manager.post(EventContinue())
