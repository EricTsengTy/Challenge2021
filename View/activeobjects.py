import pygame as pg
import os.path
import math

import Model.GameObject.player as model_player
from View.utils import scale_surface, load_image, resize_surface, rotate_surface
from pygame.math import Vector2
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

    def draw(self, screen, pos, timer):
        self.frame_index_to_draw = (timer // self.delay_of_frames) % len(self.frames)
        
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(center=pos),
        )


class View_Coffee(__Object_base):
    frames = tuple(
                pg.transform.rotate(
                    scale_surface(
                        load_image(os.path.join(Const.IMAGE_PATH, 'attack', f'attack_coffee{_i+1}.png'))
                        , 0.3
                    ), 72 * _i
                )
                for _i in range(5)
            )
    last_frames = tuple(
                pg.transform.rotate(
                    scale_surface(
                        load_image(os.path.join(Const.IMAGE_PATH, 'attack', f'attack_coffee5.png'))
                        , 0.3
                    ), 72 * _i
                )
                for _i in range(5)
            )

    @classmethod
    def init_convert(cls):
        cls.frames = tuple(_frame.convert_alpha() for _frame in cls.frames)
    
    def __init__(self, delay_of_frames):
        self.delay_of_frames = delay_of_frames

    def draw(self, screen, pos, timer):
        self.frame_index_to_draw = timer // self.delay_of_frames
        if self.frame_index_to_draw >= len(self.frames):
            screen.blit(
                self.last_frames[self.frame_index_to_draw % len(self.frames)],
                self.last_frames[self.frame_index_to_draw % len(self.frames)].get_rect(center=pos)
            )
        else:
            screen.blit(
                self.frames[self.frame_index_to_draw],
                self.frames[self.frame_index_to_draw].get_rect(center=pos)
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

class View_players(__Object_base):
    
    standing_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players' , 'standing', Const.PLAYER_STANDING_PICS[_i])), 
            Const.PLAYER_WIDTH,Const.PLAYER_HEIGHT
        )
        for _i in range(1)
    )

    walk_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'move_right', f'right_move-{_i+1}.png')),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        ) 
        for _i in range(12)
    )

    jump_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'jump_drop', f'main_chracter_jump_drop-{_i+1}.png')),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(12)
    )

    keep_item_images = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'special_attack_keep', Const.SPECIAL_ATTACK_KEEP_PICS[_i])),
            Const.ITEM_BOX_SIZE, Const.ITEM_BOX_SIZE
        ) 
        for _i in range(6)
    )

    @classmethod
    def init_convert(cls):
        cls.frames = tuple( frame.convert_alpha() for frame in cls.frames)
        cls.keep_item_images = tuple( img.convert_alpha() for img in cls.keep_item_images)

    def __init__(self, model, delay_of_frames):
        self.model = model
        self.delay_of_frames = delay_of_frames
        self.timer = [0, 0, 0, 0]
        self.status = ['standing', 'standing', 'standing', 'standing']
    
    def draw(self, screen):
        for player in self.model.players:
            
            # player itself
            if player.is_standing():
                self.status[player.player_id] = 'standing'
                self.timer[player.player_id] = 0
                screen.blit(self.standing_frames[0],
                    self.standing_frames[0].get_rect(center=player.center))
            elif player.jump_count > 0:
                if self.status[player.player_id] == 'jump':
                    self.timer[player.player_id] += 1
                else:
                    self.status[player.player_id] = 'jump'
                    self.timer[player.player_id] = 0
                self.frame_index_to_draw = (self.timer[player.player_id] // self.delay_of_frames) % len(self.jump_frames)
                screen.blit(
                    self.jump_frames[self.frame_index_to_draw],
                    self.jump_frames[self.frame_index_to_draw].get_rect(center=player.center),
                )
            else:
                if self.status[player.player_id] == 'walk':
                    self.timer[player.player_id] += 1
                else:
                    self.status[player.player_id] = 'walk'
                    self.timer[player.player_id] = 0
                self.frame_index_to_draw = (self.timer[player.player_id] // self.delay_of_frames) % len(self.walk_frames)
                screen.blit(
                    self.walk_frames[self.frame_index_to_draw],
                    self.walk_frames[self.frame_index_to_draw].get_rect(center=player.center),
                )
            '''
            status = 0 if player.face == Const.DIRECTION_TO_VEC2['right'] else 1
            screen.blit(self.images[Const.PICS_PER_PLAYER*player.player_id + status],
                self.images[Const.PICS_PER_PLAYER*player.player_id + status].get_rect(center=player.center))
            '''
            # blood
            pg.draw.rect(screen, Const.HP_BAR_COLOR[1], [player.left, player.top-10, player.rect.width*player.blood/Const.PLAYER_FULL_BLOOD, 5])
            # empty hp bar
            pg.draw.rect(screen, Const.HP_BAR_COLOR[0], [player.left, player.top-10, player.rect.width, 5], 2)

            #item frame
            pg.draw.rect(screen, Const.ITEM_BOX_COLOR, [player.left-20, player.top-15, Const.ITEM_BOX_SIZE, Const.ITEM_BOX_SIZE], 2)
            #item
            if player.keep_item_type != '':
                screen.blit(self.keep_item_images[Const.SPECIAL_ATTACK_KEEP_TO_NUM[player.keep_item_type]],
                    self.keep_item_images[Const.SPECIAL_ATTACK_KEEP_TO_NUM[player.keep_item_type]].get_rect(topleft=(player.left-20, player.top-15)))
