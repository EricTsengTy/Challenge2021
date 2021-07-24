import os.path
import pygame as pg
import numpy as np
from View.utils import scale_surface, load_image, resize_surface
import Const
import random

class Animation_base():
    def __init__(self, delay_of_frames, **pos):
        self._timer = 0
        self.expired = False

class Greeting_from_audience(Animation_base):
    
    pg.font.init()
    fonts = [ pg.font.Font(None, 24+12* _i ) for _i in range(1,4)]
    monospace_font = [pg.font.SysFont("monospace", 24+12*_i) for _i in range(1,4)]
    subtitles = [
        'printf("Hello World!");', 'console.log("Hello World!")', 'System.out.println("Hello World!");','print("Hello World!")','cout<<"Hello World!"<<endl;', 
    ]
    colors = [pg.Color('white'), pg.Color('yellow'), pg.Color('red'), pg.Color('blue'), pg.Color('green'), pg.Color('pink'), pg.Color('black')]
    positions = [Const.ARENA_SIZE[1] // 20 * _i for _i in range(20)]

    def __init__(self, delay_of_frames, speed):
        self._timer = 0
        self.delay_of_frames = delay_of_frames
        self.speed = speed
        self.expire_time = 10*Const.FPS
        self.expired = False
        self.text_surfaces = tuple(random.choice(self.fonts).render(random.choice(self.subtitles), 1, random.choice(self.colors)) for _i in range(40))
        self.text_surfaces = tuple(surface.convert_alpha() for surface in self.text_surfaces)
        self.text_center = [ [random.randint(Const.ARENA_SIZE[0], 2*Const.ARENA_SIZE[0]), random.choice(self.positions)] for _i in range(40)]
    
    def update(self):
        self._timer += 1

        if self._timer == self.expire_time:
            self.expired = True
        
        if self._timer % self.delay_of_frames == 0:
            for i in range(40):
                self.text_center[i][0] -= self.speed * self.delay_of_frames

    
    def draw(self, screen, update=True):
        for i in range(40):
            screen.blit(self.text_surfaces[i], (self.text_center[i][0], self.text_center[i][1]))
        
        if update: self.update()
    

    '''
    font = pg.font.Font(None, 36)
    text_surface = font.render("Press [space] to start ...", 1, pg.Color('gray88'))
    text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
    self.screen.blit(text_surface, text_surface.get_rect(center=text_center))
    '''

class Greeting_from_prog(Animation_base):
    _how_many = 0
    @classmethod
    def new_obj(cls):
        cls._how_many += 1
        return cls._how_many
    
    def __init__(self,delay_of_frames):
        super().__init__(delay_of_frames)
        self.expired_time = 160
        head_font = pg.font.SysFont(None, 200)
        self.text_surface = head_font.render('Hello World!', True, (0, 0, 0))
        self.text_surface = self.text_surface.convert_alpha()
        self.num = self.new_obj()

    def rolling(self,source_arr):
        return np.roll(source_arr,self._timer*-10,axis=1)

    def RGB_shift(self,pixel_arr):
        R = pixel_arr[:,:,0]
        G = pixel_arr[:,:,1]
        B = pixel_arr[:,:,2]
        
        a,b,c = random.randint(-13,13),random.randint(-13,13),random.randint(-13,13)
        if a > 0   : pixel_arr[a:,:,0] = R[:-a,:]
        elif a < 0 : pixel_arr[:a,:,0] = R[-a:,:]
        if b > 0   : pixel_arr[b:,:,1] = G[:-b,:]
        elif b < 0 : pixel_arr[:b,:,1] = G[-b:,:]
        if c > 0   : pixel_arr[c:,:,2] = B[:-c,:]
        elif c < 0 : pixel_arr[:c,:,2] = B[-c:,:]
    
    def shifting(self,pixel_arr):
        for _ in range(5):
            stripe_width = random.randint(20,30)
            stripe_pos = random.randint(0,self.canvas_size[1]-1)
            stripe_amount = random.randint(5,30)
            pixel_arr[stripe_amount:,stripe_pos:stripe_pos+stripe_width] = pixel_arr[:-stripe_amount,stripe_pos:stripe_pos+stripe_width]
        
        for _ in range(10):
            stripe_width = random.randint(0,10)
            stripe_pos = random.randint(0,self.canvas_size[1]-1)
            stripe_amount = random.randint(5,30)
            pixel_arr[stripe_amount:,stripe_pos:stripe_pos+stripe_width] = pixel_arr[:-stripe_amount,stripe_pos:stripe_pos+stripe_width]

    def scrollY(self, screen, amount):
        width, height = screen.get_size()
        copySurf = screen.convert()
        screen.blit(copySurf, (0, amount))
        if amount < 0:
            screen.blit(copySurf, (0, height + amount), (0, 0, width, -amount))
        else:
            screen.blit(copySurf, (0, 0), (0, height-amount, width, amount))

    def update(self):
        self._timer += 1
        if self._timer == self.expired_time:
            self.expired = True

    def draw(self, screen, update):
        if self.num != self._how_many:
            self.expired = True
            return
        if update: self.update()
        self.canvas_size = screen.get_size()
        self.scrollY(screen,(self._timer%80)*-10) # default to scroll -10 pixel
        screen.blit(self.text_surface, self.text_surface.get_rect( center =  screen.get_rect().center ))

        source_arr = pg.surfarray.pixels3d(screen)
        self.RGB_shift(source_arr)
        self.shifting(source_arr)

class Greeeting_from_player(Animation_base):
    _how_many = 0
    chatlog_img = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'hello_world', f'hello_world3_{_i+1}.png'))
        for _i in range(4)
    )

    fliped_chatlog_img = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'hello_world', f'hello_world3_{_i+1}_mir.png'))
        for _i in range(4)
    )

    @classmethod
    def init_convert(cls):
        cls.chatlog_img = tuple(img.convert_alpha() for img in cls.chatlog_img)
        cls.fliped_chatlog_img = tuple(img.convert_alpha() for img in cls.fliped_chatlog_img)

    @classmethod
    def new_obj(cls):
        cls._how_many += 1
        return cls._how_many
    
    def __init__(self, model):
        self.expire_time = 10*Const.FPS
        self.refresh_time = 2*Const.FPS
        self.expired = False
        self._timer = 0
        self.model = model
        self.chatlogs = [0,1,2,3]
        self.num = self.new_obj()

    def update(self):
        self._timer += 1

        if self._timer % self.refresh_time == 0:
            random.shuffle(self.chatlogs)
        if self._timer == self.expire_time:
            self.expired = True

    def draw(self, screen,  update=True):
        if self.num != self._how_many :
            self.expired = True
            return
        for player in self.model.players:
            if player.face == Const.DIRECTION_TO_VEC2['left']:
                screen.blit(
                    self.chatlog_img[self.chatlogs[player.player_id]], self.chatlog_img[self.chatlogs[player.player_id]].get_rect(bottomright=player.rect.topleft)
                )
            else:
                screen.blit(
                    self.fliped_chatlog_img[self.chatlogs[player.player_id]], self.fliped_chatlog_img[self.chatlogs[player.player_id]].get_rect(bottomleft=player.rect.topright)
                )
        if update: self.update()

def init_animation():
    Greeeting_from_player.init_convert()