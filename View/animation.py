import pygame as pg

from View.utils import scale_surface, load_image, resize_surface
import Const
import random

class Animation_base():
    def __init__(self, delay_of_frames, **pos):
        self._timer = 0
        self.expired = False

class Animation_raster():
    frames = tuple()

    @classmethod
    def init_convert(cls):
        cls.frames = tuple( _frame.convert_alpha() for _frame in cls.frames)

    def __init__(self, delay_of_frames, expire_time, **pos):
        self._timer = 0
        self.delay_of_frames = delay_of_frames
        self.frame_index_to_draw = 0
        self.expire_time = expire_time
        self.expired = False
    
    def update(self):
        self._timer += 1

        if self._timer == self.expire_time:
            self.expire = True
        elif self._timer % self.delay_of_frames == 0:
            self.frame_index_to_draw = (self.frame_index_to_draw + 1) % len(self.frames)

    def draw(self, screen, update=True):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(**self.pos),
        )
        
        if update: self.update()


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