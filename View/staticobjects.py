from View.players import player_frames
import pygame as pg
import os.path

from View.utils import Text, scale_surface, load_image, resize_surface, rotate_surface
from pygame.math import Vector2
import Const

class __Object_base():
    images = tuple()

    @classmethod
    def init_convert(cls):
        cls.images = tuple(img.convert_alpha() for img in cls.images)
    
    def __init__(self, model):
        self.model = model

class View_menu(__Object_base):
	menu = resize_surface(load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'start.png')),
			Const.ARENA_SIZE[0], Const.ARENA_SIZE[1])

	@classmethod
	def init_convert(cls):
		cls.stage = cls.stage.convert_alpha()
	
	def draw(self, screen):
		screen.blit(self.menu, (0,0))

class View_tutorial(__Object_base):
	tutorial = resize_surface(load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'tutorial.png')),
			Const.ARENA_SIZE[0], Const.ARENA_SIZE[1])

	@classmethod
	def init_convert(cls):
		cls.stage = cls.stage.convert_alpha()
	
	def draw(self, screen):
		screen.blit(self.tutorial, (0,0))

class View_stage(__Object_base):
    stage = resize_surface(load_image(os.path.join(Const.IMAGE_PATH, 'stage', 'stage.png')),
        Const.ARENA_SIZE[0], Const.ARENA_SIZE[1])

    @classmethod
    def init_convert(cls):
        cls.stage = cls.stage.convert_alpha()

    def draw(self, screen):
        #screen.fill(Const.BACKGROUND_COLOR)
        screen.blit(self.stage, (0, 0))

class View_platform(__Object_base):
    block = resize_surface(load_image(os.path.join(Const.IMAGE_PATH, 'floor', 'floor_block.png')),
        Const.GROUND_SIZE, Const.GROUND_SIZE)


    @classmethod
    def init_convert(cls):
        cls.block = cls.block.convert_alpha()

    def draw(self, screen):
        for ground in Const.GROUND_POSITION[:-1]:
            #(left, top, width, height)
            block_num = ground[2] // Const.GROUND_SIZE
            for _i in range(block_num):
                screen.blit(self.block, self.block.get_rect(topleft=(ground[0] + Const.GROUND_SIZE * _i , ground[1])))

class View_Arrow(__Object_base):
    images = tuple(
        rotate_surface(
            resize_surface(
                load_image(os.path.join(Const.IMAGE_PATH, 'attack', 'attack_dos.png')),
                Const.ARROW_SIZE ,Const.ARROW_SIZE
            ), 180 + 72*_i
        )
        for _i in range(5)
    )

    @classmethod
    def init_convert(cls):
        cls.images = tuple( img.convert_alpha() for img in cls.images)
    
    def draw(self, screen, pos, speed):
        angle = round(Vector2().angle_to(speed))
        if angle in [90,162,-54,126,18]:
            screen.blit(self.images[(5-((angle+270)//72))%5], self.images[(5-((angle+270)//72))%5].get_rect(center=pos))
        else:
            img = rotate_surface(self.images[0], -angle+90)
            screen.blit(img, img.get_rect(center=pos))

class View_Lightning(__Object_base):
    images = tuple(
        rotate_surface(
            resize_surface(
                load_image(os.path.join(Const.IMAGE_PATH, 'attack', 'attack_lightning.png')),
                Const.LIGHTNING_SIZE ,Const.LIGHTNING_SIZE
            ), -90 - 45*_i
        )
        for _i in range(8)
    )

    @classmethod
    def init_convert(cls):
        cls.images = tuple( img.convert_alpha() for img in cls.images)
    
    def draw(self, screen, pos, dist):
        for _i in range(8):
            screen.blit(self.images[_i], self.images[_i].get_rect(center=(pos - dist * Vector2(1, 0).rotate(45 * _i))))

class View_Item(__Object_base):
    images = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'prop', Const.PROP_PICS[_i])),
            Const.ITEM_WIDTH, Const.ITEM_HEIGHT
        )
        for _i in range(13)
    )
    prop_image = resize_surface(
        load_image(os.path.join(Const.IMAGE_PATH, 'prop', 'prop.png')),
        Const.ITEM_WIDTH//5, Const.ITEM_HEIGHT//5
    )
    @classmethod
    def init_convert(cls):
        cls.images = tuple( img.convert_alpha() for img in cls.images)
        cls.prop_image = cls.prop_image.convert_alpha()
    def draw(self, screen, rect, item_type):
        _pic = Const.ITEM_TYPE_LIST.index(item_type)
        screen.blit(self.images[_pic], self.images[_pic].get_rect(center=rect.center))
        screen.blit(self.prop_image, self.prop_image.get_rect(bottomleft=rect.bottomleft))

class View_Pause(__Object_base):
    pause_window = scale_surface(load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'pause.png')), 0.7)

    @classmethod
    def init_convert(cls):
        cls.pause_window = cls.pause_window.convert_alpha()
    
    def draw(self, screen):
        screen.blit(self.pause_window, self.pause_window.get_rect(center=(Const.ARENA_SIZE[0]/2, Const.ARENA_SIZE[1]/2)))

class View_Scoreboard(__Object_base):
    board = resize_surface(
        load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'result.png')), 
        Const.ARENA_SIZE[0], Const.ARENA_SIZE[1]
    )
    winner_crown = load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'crown.png'))
    gray_bg = resize_surface(
        load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'transparent_gray.png')),
        Const.ARENA_SIZE[0], Const.ARENA_SIZE[1]
    )

    @classmethod
    def init_convert(cls):
        cls.board = cls.board.convert_alpha()
        cls.winner_crown = cls.winner_crown.convert_alpha()
        cls.gray_bg = cls.gray_bg.convert_alpha()
        cls.draw_gray_bg = True

    def draw(self, screen):
        #only draw gray background one time
        if self.draw_gray_bg:
            screen.blit(self.gray_bg, (0, 0))
            self.draw_gray_bg = False

        #draw main board
        screen.blit(self.board, (0, 0))
        
        player_score = []
        '''
        for player in self.model.players:
            player_score.append(player.score)
        '''
        player_score = [10, 10000, 1000, 2000] #test score
        text_interval = Const.ARENA_SIZE[0]/8.35
        text_start = Const.ARENA_SIZE[0]/2 - text_interval*1.75
        text_top = Const.ARENA_SIZE[1]/1.75
        for i in range(len(player_score)):
            if player_score[i] == max(player_score):
                #draw winner crown
                screen.blit(self.winner_crown, (text_start + i*text_interval, Const.ARENA_SIZE[1]/2.8))
            #draw score
            score_text = Text(str(player_score[i]), 36, pg.Color('white'))
            score_text.blit(screen, topleft=(text_start + i*text_interval, text_top))

class View_ColorPicker(__Object_base):
    menu = resize_surface(load_image(os.path.join(Const.IMAGE_PATH, 'menu', 'select_color.png')), 
        Const.ARENA_SIZE[0], Const.ARENA_SIZE[1])

    player_imgs = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players' , 'standing', 'standing-{:02d}.png'.format(_i+1)))
        for _i in range(1)
    )*Const.COLOR_TABLE_SIZE

    def fill_color(self,player_img, color):
        "get a pygame Surface of player image return the colored Surface"
        result_img = player_img.convert_alpha()
        px_arr = pg.surfarray.pixels2d(result_img)
        px_arr[px_arr==4288534508] = result_img.map_rgb(color)
        return result_img
    
    
    @classmethod
    def init_convert(cls):
        cls.menu = cls.menu.convert_alpha()
	
    def __init__(self, model):
        super().__init__(model)
        self.player_imgs = tuple(
            resize_surface(
                self.fill_color(img, pg.Color(Const.COLOR_TABLE[_i])), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img, _i in zip(self.player_imgs,range(Const.COLOR_TABLE_SIZE))
        )


    def draw(self, screen):
        screen.blit(self.menu, (0,0))
        color_center = [(470+80*_i,450) for _i in range((Const.COLOR_TABLE_SIZE+1)//2)] + [(505+80*_i,535) for _i in range(Const.COLOR_TABLE_SIZE//2)]
        player_center = [(473+145*_i,300) for _i in range(4)]

        for player, _i in zip(self.model.players, range(4)):
            #index = Const.COLOR_TABLE.index(player.color)
            pg.draw.circle(screen, Const.PLAYER_PICKER_COLOR[_i], color_center[player.color_index], 38)
            screen.blit(
                self.player_imgs[player.color_index],
                self.player_imgs[player.color_index].get_rect(center=player_center[_i])
            )

        for _i in range(Const.COLOR_TABLE_SIZE):
            pg.draw.circle(screen, pg.Color(Const.COLOR_TABLE[_i]), color_center[_i], 35)

def init_staticobjects():
    View_stage.init_convert()
    View_platform.init_convert()
    View_Arrow.init_convert()
    View_Lightning.init_convert()
    View_Item.init_convert()
    View_Pause.init_convert()
    View_Scoreboard.init_convert()
    View_ColorPicker.init_convert()
