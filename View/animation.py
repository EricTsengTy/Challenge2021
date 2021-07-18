import pygame as pg
import numpy as np
import Const
import random

class Animation_base():
    def __init__(self, delay_of_frames):
        self._timer = 0
        self.expired = False
        self.delay_of_frames = delay_of_frames

class Animation_hello_world(Animation_base):
    
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
    
    def __init__(self,delay_of_frames):
        super().__init__(delay_of_frames)
        self.expired_time = 80
        font = pg.font.SysFont(None, 200)
        self.text_surface = font.render('Hello World!', True, (0, 0, 0))
        self.text_surface = self.text_surface.convert_alpha()

    def rolling(self,source_arr):
        return np.roll(source_arr,self._timer*-10,axis=1)

    def RGB_shift(self,source_arr):
        R = source_arr[:,:,0]
        G = source_arr[:,:,1]
        B = source_arr[:,:,2]
        result_arr = np.zeros((*self.canvas_size,3))
        
        a,b,c = random.randint(-13,13),random.randint(-13,13),random.randint(-13,13)
        if a > 0   : result_arr[a:,:,0] = R[:-a,:]
        elif a < 0 : result_arr[:a,:,0] = R[-a:,:]
        if b > 0   : result_arr[b:,:,1] = G[:-b,:]
        elif b < 0 : result_arr[:b,:,1] = G[-b:,:]
        if c > 0   : result_arr[c:,:,2] = B[:-c,:]
        elif c < 0 : result_arr[:c,:,2] = B[-c:,:]
        
        return result_arr
    
    def shifting(self,source_arr):
        result_arr = np.zeros((*self.canvas_size,3))
        result_arr[:,:,:] = source_arr[:,:,:]
        for _ in range(1):
            stripe_width = 20
            stripe_pos = 2
            stripe_amount = 5
            result_arr[stripe_amount:,stripe_pos:stripe_pos+stripe_width] = source_arr[:-stripe_amount,stripe_pos:stripe_pos+stripe_width]
        
        for _ in range(0):
            stripe_width = random.randint(0,10)
            stripe_pos = random.randint(0,self.canvas_size[1]-1)
            stripe_amount = random.randint(5,30)
            result_arr[stripe_amount:,stripe_pos:stripe_pos+stripe_width] = source_arr[:-stripe_amount,stripe_pos:stripe_pos+stripe_width]
        return result_arr
    
    def update(self):
        self._timer += 1

        if self._timer == self.expired_time:
            self.expired = True

    def Hello_world(self,screen):
        HW_pos = (100,250)
        screen.blit(self.text_surface, HW_pos)

    def draw(self, screen, update):
        if update: self.update()
        self.canvas_size = screen.get_size()

        source_arr = pg.surfarray.array3d(screen)
        source_arr = self.rolling(source_arr)
        
        source_arr = self.RGB_shift(source_arr)
        source_arr = self.shifting(source_arr)
        result = pg.surfarray.make_surface(source_arr)
        screen.blit(result,(0,0))
        self.Hello_world(screen)