from os import walk
import pygame as pg
import os.path

from pygame.display import update

from View.utils import scale_surface, load_image, resize_surface
import Const
class __Object_base():
    
    frames = tuple()
    
    @classmethod
    def init_convert(cls):
        cls.frames = tuple( _frame.convert_alpha() for _frame in cls.frames)

    def __init__(self, delay_of_frames):
        self._timer = 0
        self.delay_of_frames = delay_of_frames
        self.frame_index_to_draw = 0
    
    def update(self):
        self._timer += 1
        
        if self._timer % self.delay_of_frames == 0:
            self.frame_index_to_draw = (self.frame_index_to_draw + 1) % len(self.frames)
    
    def draw(self, screen, pos):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(center=pos),
        )
        self.update()

class View_Bug(__Object_base):
    frames = tuple(
        pg.transform.rotate(
            resize_surface(
                load_image(os.path.join(Const.IMAGE_PATH, 'attack', 'attack_bug.png')),
                Const.BUG_WIDTH, Const.BUG_HEIGHT
            ), 72 * _i
        )
        for _i in range(5)
    )
    
    @classmethod
    def init_convert(cls):
        cls.frames = tuple(_frame.convert_alpha() for _frame in cls.frames)
    
    def __init__(self, delay_of_frames):
        self.delay_of_frames = delay_of_frames
    
    @staticmethod
    def mid_point(a,b):
        return ((a[0]+b[0])/2,(a[1]+b[1])/2)

    def draw(self, screen, pos, timer, track):
        self.frame_index_to_draw = (timer // self.delay_of_frames) % len(self.frames)
        
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(center=pos),
        )
        track_timer = timer-1
        tmp = 0
        for _i in range( track_timer+5, track_timer+50 ,5 ):
            start_point = track[  _i%50 ]
            end_point = self.mid_point( track[(_i+5)%50], track[_i%50])
            pg.draw.line(screen, (180,0,0), start_point, end_point, width=4)
            tmp += 1

class View_Coffee(__Object_base):
    Frames = tuple(
                pg.transform.rotate(
                    scale_surface(
                        load_image(os.path.join(Const.IMAGE_PATH, 'attack', f'attack_coffee{_i+1}.png'))
                        , 0.5
                    ), 72 * _i
                )
                for _i in range(5)
            )
    Last_Frames = tuple(
                pg.transform.rotate(
                    scale_surface(
                        load_image(os.path.join(Const.IMAGE_PATH, 'attack', f'attack_coffee5.png'))
                        , 0.5
                    ), 72 * _i
                )
                for _i in range(5)
            )
    
    @staticmethod
    def translucent(img,alpha):
        "change player's opacity (img will be use as invisible player)"
        result_img = img.convert_alpha()
        result_img.fill((255, 255, 255, alpha), None, pg.BLEND_RGBA_MULT)
        return result_img

    @classmethod
    def init_convert(cls):
        cls.frames = []
        cls.last_frames = []
        for i in range(1,6):
            cls.frames.append( 
                tuple( cls.translucent( _frame, 255*i//5 ) for _frame in cls.Frames )
            )
            cls.last_frames.append( 
                tuple( cls.translucent( _frame, 255*i//5 ) for _frame in cls.Last_Frames )
            )
    def __init__(self, delay_of_frames):
        self.delay_of_frames = delay_of_frames

    def draw(self, screen, pos, timer,track):
        gaps = [5,9,13,16,19]
        self.frame_index_to_draw = (timer+19) // self.delay_of_frames
        for (idx,gap) in enumerate(gaps):
            
            pos = track[(timer+gap)%20]
            if self.frame_index_to_draw >= len(self.Frames):
                screen.blit(
                    self.last_frames[idx][self.frame_index_to_draw % len(self.Frames)],
                    self.last_frames[idx][self.frame_index_to_draw % len(self.Frames)].get_rect(center=pos)
                )
            else:
                screen.blit(
                    self.frames[idx][self.frame_index_to_draw],
                    self.frames[idx][self.frame_index_to_draw].get_rect(center=pos)
                )
            
    
class View_Fireball(__Object_base):
    frames = tuple(
            resize_surface(
                load_image(os.path.join(Const.IMAGE_PATH, 'attack', f'attack_fireball{_i+1}.png')),
                Const.FIREBALL_RADIUS*2, Const.FIREBALL_RADIUS*2
            )
            for _i in range(2)
        )
    fliped_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in frames
        )

    @classmethod
    def init_convert(cls):
        cls.frames = tuple(_frame.convert_alpha() for _frame in cls.frames)
    
    def __init__(self, delay_of_frames):
        self.delay_of_frames = delay_of_frames

    def draw(self, screen, pos, timer, speed):
        self.frame_index_to_draw = (timer // self.delay_of_frames) % len(self.frames)
        if speed.x > 0:
            screen.blit(
                self.frames[self.frame_index_to_draw],
                self.frames[self.frame_index_to_draw].get_rect(center=pos),
            )
        else:
            screen.blit(
                self.fliped_frames[self.frame_index_to_draw],
                self.fliped_frames[self.frame_index_to_draw].get_rect(center=pos),
            )

class View_Fireball(__Object_base):
    frames = tuple(
            resize_surface(
                load_image(os.path.join(Const.IMAGE_PATH, 'attack', f'attack_fireball{_i+1}.png')),
                Const.FIREBALL_RADIUS*2, Const.FIREBALL_RADIUS*2
            )
            for _i in range(2)
        )
    fliped_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in frames
        )

    @classmethod
    def init_convert(cls):
        cls.frames = tuple(_frame.convert_alpha() for _frame in cls.frames)
    
    def __init__(self, delay_of_frames):
        self.delay_of_frames = delay_of_frames

    def draw(self, screen, pos, timer, speed):
        self.frame_index_to_draw = (timer // self.delay_of_frames) % len(self.frames)
        if speed.x > 0:
            screen.blit(
                self.frames[self.frame_index_to_draw],
                self.frames[self.frame_index_to_draw].get_rect(center=pos),
            )
        else:
            screen.blit(
                self.fliped_frames[self.frame_index_to_draw],
                self.fliped_frames[self.frame_index_to_draw].get_rect(center=pos),
            )

class View_Lightning(__Object_base):
    frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'lightning', 'lightning-{:02d}.png'.format(_i))),
            150 ,800
        ) for _i in range(1,10)
    )
    gray_bg = resize_surface(
        load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'transparent_gray.png')),
        Const.ARENA_SIZE[0], Const.ARENA_SIZE[1]
    )

    def __init__(self, delay_of_frames):
        self.delay_of_frames = delay_of_frames

    @classmethod
    def init_convert(cls):
        cls.frames = tuple( frame.convert_alpha() for frame in cls.frames)
        cls.gray_bg = cls.gray_bg.convert_alpha()
    def draw(self, screen, dest, timer, pos):
        pos = (pos[0], dest+Const.LIGHTNING_HEIGHT)
        self.frame_index_to_draw = (timer // self.delay_of_frames) % len(self.frames)
        screen.blit(self.gray_bg, (0, 0))
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(bottomleft=pos),
        )
        

class View_Tornado(__Object_base):
    frames = tuple(
            resize_surface(
                load_image(os.path.join(Const.IMAGE_PATH, 'attack', f'attack_fan{_i+1}.png')),
                Const.TORNADO_WIDTH, Const.TORNADO_HEIGHT
            )
            for _i in range(4)
        )
    fliped_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in frames
        )

    @classmethod
    def init_convert(cls):
        cls.frames = tuple(_frame.convert_alpha() for _frame in cls.frames)
    
    def __init__(self, delay_of_frames):
        self.delay_of_frames = delay_of_frames

    def draw(self, screen, pos, timer, speed):
        self.frame_index_to_draw = (timer // self.delay_of_frames) % len(self.frames)
        if speed.x > 0:
            screen.blit(
                self.frames[self.frame_index_to_draw],
                self.frames[self.frame_index_to_draw].get_rect(center=pos),
            )
        else:
            screen.blit(
                self.fliped_frames[self.frame_index_to_draw],
                self.fliped_frames[self.frame_index_to_draw].get_rect(center=pos),
            )


class View_ColorPicker(__Object_base):
    menu = resize_surface(load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'select_color.png')), 
        Const.ARENA_SIZE[0], Const.ARENA_SIZE[1])

    walk_frames = [tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'right_move', 'right_move-{:02d}.png'.format(_i+1)))
        for _i in range(8)
    )]*Const.COLOR_TABLE_SIZE

    def fill_color(self,player_img, color):
        "get a pygame Surface of player image return the colored Surface"
        result_img = player_img.convert_alpha()
        px_arr = pg.surfarray.pixels2d(result_img)
        px_arr[px_arr==4288534508] = result_img.map_rgb(color)
        return result_img
    
    
    @classmethod
    def init_convert(cls):
        cls.menu = cls.menu.convert_alpha()
	
    def __init__(self, model, delay_of_frames):
        self.model = model
        self.delay_of_frames = delay_of_frames
        self._timer = [0,0,0,0]
        self.frame_index_to_draw = [0,0,0,0]
        self.color_center = [(470+80*_i,450) for _i in range((Const.COLOR_TABLE_SIZE+1)//2)] + [(505+80*_i,535) for _i in range(Const.COLOR_TABLE_SIZE//2)]
        self.player_center = [(473+145*_i,300) for _i in range(4)]
        
        for _i in range(Const.COLOR_TABLE_SIZE):
            self.walk_frames[_i] = tuple(
                resize_surface(
                    self.fill_color(img, pg.Color(Const.COLOR_TABLE[_i])), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
                )  for img in self.walk_frames[_i]
            )
              
        self.selection_icon = tuple(
            resize_surface(
                load_image(
                    os.path.join(Const.IMAGE_PATH, 'selection_icon' , 'selection_icon-{:02d}.png'.format(_i+1))
                ),60, 60
            )for _i in range(4)
        )

    def update(self):
        
        for _i in range(4):
            self._timer[_i] += 1
        
            if self._timer[_i] % self.delay_of_frames == 0:
                self.frame_index_to_draw[_i] = (self.frame_index_to_draw[_i] + 1) % len(self.walk_frames[_i])

    @staticmethod
    def tuple_plus(a,b):
        return (a[0]+b[0],a[1]+b[1])

    def draw(self, screen):
        screen.blit(self.menu, (0,0))

        for _i in range(Const.COLOR_TABLE_SIZE):
            pg.draw.circle(screen, pg.Color(Const.COLOR_TABLE[_i]), self.color_center[_i], 28)
        
        for player, _i in zip(self.model.players, range(4)):
            screen.blit(
                self.walk_frames[player.color_index][self.frame_index_to_draw[_i]],
                self.walk_frames[player.color_index][self.frame_index_to_draw[_i]].get_rect(center=self.player_center[_i])
            )
            screen.blit(
                self.selection_icon[_i],
                self.selection_icon[_i].get_rect(center=self.color_center[player.color_index])
            )
        self.update()

def init_activeobjects():
    View_Bug.init_convert()
    View_Coffee.init_convert()
    View_Fireball.init_convert()
    View_Tornado.init_convert()
    View_ColorPicker.init_convert()
    View_Lightning.init_convert()