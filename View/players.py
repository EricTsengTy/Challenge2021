import pygame as pg
import os.path

from View.utils import load_image, resize_surface
import Const
import numpy as np

class player_frames():
    # frames uncolored in cls (is the same between players)
    # frame colored in self (can be different between players)

    standing_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players' , 'standing', 'standing-{:02d}.png'.format(_i+1)))
        for _i in range(1)
    )

    poison_standing_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players' , 'standing', 'poison_standing-{:02d}.png'.format(_i+1)))
        for _i in range(1)
    )

    walk_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'right_move', 'right_move-{:02d}.png'.format(_i+1)))
        for _i in range(8)
    )

    poison_walk_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'right_move', 'poison_right_move-{:02d}.png'.format(_i+1)))
        for _i in range(8)
    )

    jump_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'jump_drop', 'jump_drop-{:02d}.png'.format(_i+1)))
        for _i in range(13)
    )

    poison_jump_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'jump_drop', 'poison_jump_drop-{:02d}.png'.format(_i+1)))
        for _i in range(13)
    )

    common_attack_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'physical_atk', 'physical_atk-{:02d}.png'.format(_i+1)))
        for _i in range(13)
    )

    poison_common_attack_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'physical_atk', 'poison_physical_atk-{:02d}.png'.format(_i+1)))
        for _i in range(13)
    )

    be_attacked_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'be_attacked', 'be_attacked-{:02d}.png'.format(_i+1)))
        for _i in range(9)
    )

    poison_be_attacked_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'be_attacked', 'poison_be_attacked-{:02d}.png'.format(_i+1)))
        for _i in range(9)
    )

    attack_fireball_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'special_atk', 'fire_ball-{:02d}.png'.format(_i+1)))
        for _i in range(13)
    )

    attack_bug_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'special_atk', 'bug-{:02d}.png'.format(_i+1)))
        for _i in range(9)
    )

    attack_coffee_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'special_atk', 'coffee-{:02d}.png'.format(_i+1)))
        for _i in range(9)
    )

    attack_ddos_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'special_atk', 'DDOS-{:02d}.png'.format(_i+1)))
        for _i in range(13)
    )

    attack_fan_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'special_atk', 'fan-{:02d}.png'.format(_i+1)))
        for _i in range(13)
    )

    attack_lightning_images = tuple(
        load_image(os.path.join(Const.IMAGE_PATH, 'players', 'special_atk', 'lightning-{:02d}.png'.format(_i+1)))
        for _i in range(13)
    )


    def fill_color(self,player_img):
        "get a pygame Surface of player image return the colored Surface"
        nb_color = self.color
        result_img = player_img.convert_alpha()
        if Const.PLAYER_COLOR_DRAWER == False:
            return result_img
        px_arr = pg.PixelArray(result_img)  
        w,h = px_arr.shape[0],px_arr.shape[1]
        for i in range(w//2,w):
            for j in range(h//8,h*3//4):
                if px_arr[i,j] == 4288534508 or px_arr[i,j] == -6432788:
                    px_arr[i,j] = nb_color
        pg.PixelArray(result_img).close()
        return result_img
    
    def draw_frames(self):
        "draw all the frames for self"
        self.standing_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.standing_images
        )
        
        self.poison_standing_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.poison_standing_images
        )

        self.walk_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.walk_images
        )

        self.poison_walk_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.poison_walk_images
        )

        self.jump_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.jump_images
        )
        
        self.poison_jump_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.poison_jump_images
        )

        self.common_attack_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.common_attack_images
        )

        self.poison_common_attack_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.poison_common_attack_images
        )

        self.be_attacked_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.be_attacked_images
        )

        self.poison_be_attacked_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.poison_be_attacked_images
        )

        self.attack_fireball_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.attack_fireball_images
        )

        self.attack_bug_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.attack_bug_images
        )

        self.attack_coffee_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.attack_coffee_images
        )

        self.attack_ddos_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.attack_ddos_images
        )

        self.attack_fan_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.attack_fan_images
        )

        self.attack_lightning_frames = tuple(
            resize_surface(
                self.fill_color(img), Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
            )  for img in self.attack_lightning_images
        )

        self.flipped_standing_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.standing_frames
        )
        self.flipped_poison_standing_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.poison_standing_frames
        )
        self.flipped_walk_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.walk_frames
        )
        self.flipped_poison_walk_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.poison_walk_frames
        )
        self.flipped_jump_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.jump_frames
        )
        self.flipped_poison_jump_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.poison_jump_frames
        )
        self.flipped_common_attack_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.common_attack_frames
        )
        self.flipped_poison_common_attack_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.poison_common_attack_frames 
        )
        self.flipped_be_attacked_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.be_attacked_frames
        )
        self.flipped_poison_be_attacked_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.poison_be_attacked_frames
        )
        self.flipped_attack_fireball_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.attack_fireball_frames
        )
        self.flipped_attack_bug_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.attack_bug_frames
        )
        self.flipped_attack_coffee_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.attack_coffee_frames
        )
        self.flipped_attack_ddos_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.attack_ddos_frames
        )
        self.flipped_attack_fan_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.attack_fan_frames
        )
        self.flipped_attack_lightning_frames = tuple(
            pg.transform.flip(_frame, True, False) for _frame in self.attack_lightning_frames
        )


    def init_convert(self):
        self.standing_frames = tuple( frame.convert_alpha() for frame in self.standing_frames)
        self.flipped_standing_frames = tuple( frame.convert_alpha() for frame in self.flipped_standing_frames)
        self.walk_frames = tuple( frame.convert_alpha() for frame in self.walk_frames)
        self.flipped_walk_frames = tuple( frame.convert_alpha() for frame in self.flipped_walk_frames)
        self.jump_frames = tuple( frame.convert_alpha() for frame in self.jump_frames)
        self.flipped_jump_frames = tuple( frame.convert_alpha() for frame in self.flipped_jump_frames)
        self.common_attack_frames = tuple( frame.convert_alpha() for frame in self.common_attack_frames)
        self.flipped_common_attack_frames = tuple( frame.convert_alpha() for frame in self.flipped_common_attack_frames)
        self.be_attacked_frames = tuple( frame.convert_alpha() for frame in self.be_attacked_frames)
        self.flipped_be_attacked_frames = tuple( frame.convert_alpha() for frame in self.flipped_be_attacked_frames)
        self.attack_fireball_frames = tuple( frame.convert_alpha() for frame in self.attack_fireball_frames)
        self.flipped_attack_fireball_frames = tuple( frame.convert_alpha() for frame in self.flipped_attack_fireball_frames)
        self.attack_bug_frames = tuple( frame.convert_alpha() for frame in self.attack_bug_frames)
        self.flipped_attack_bug_frames = tuple( frame.convert_alpha() for frame in self.flipped_attack_bug_frames)
        self.attack_coffee_frames = tuple( frame.convert_alpha() for frame in self.attack_coffee_frames)
        self.flipped_attack_coffee_frames = tuple( frame.convert_alpha() for frame in self.flipped_attack_coffee_frames)
        self.attack_ddos_frames = tuple( frame.convert_alpha() for frame in self.attack_ddos_frames)
        self.flipped_attack_ddos_frames = tuple( frame.convert_alpha() for frame in self.flipped_attack_ddos_frames)
        self.attack_fan_frames = tuple( frame.convert_alpha() for frame in self.attack_fan_frames)
        self.flipped_attack_fan_frames = tuple( frame.convert_alpha() for frame in self.flipped_attack_fan_frames)
        self.attack_lightning_frames = tuple( frame.convert_alpha() for frame in self.attack_lightning_frames)
        self.flipped_attack_lightning_frames = tuple( frame.convert_alpha() for frame in self.flipped_attack_lightning_frames)
        self.poison_standing_frames = tuple( frame.convert_alpha() for frame in self.poison_standing_frames)
        self.flipped_poison_standing_frames = tuple( frame.convert_alpha() for frame in self.flipped_poison_standing_frames)
        self.poison_walk_frames = tuple( frame.convert_alpha() for frame in self.poison_walk_frames)
        self.flipped_poison_walk_frames = tuple( frame.convert_alpha() for frame in self.flipped_poison_walk_frames)
        self.poison_jump_frames = tuple( frame.convert_alpha() for frame in self.poison_jump_frames)
        self.flipped_poison_jump_frames = tuple( frame.convert_alpha() for frame in self.flipped_poison_jump_frames)
        self.poison_common_attack_frames = tuple( frame.convert_alpha() for frame in self.poison_common_attack_frames)
        self.flipped_poison_common_attack_frames = tuple( frame.convert_alpha() for frame in self.flipped_poison_common_attack_frames)
        self.poison_be_attacked_frames = tuple( frame.convert_alpha() for frame in self.poison_be_attacked_frames)
        self.flipped_poison_be_attacked_frames = tuple( frame.convert_alpha() for frame in self.flipped_poison_be_attacked_frames)

    def __init__(self,color):
        self.color =  color
        self.draw_frames()
        self.init_convert()


class View_players():

    keep_item_images = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'special_attack_keep', Const.SPECIAL_ATTACK_KEEP_PICS[_i])),
            Const.ITEM_BOX_SIZE, Const.ITEM_BOX_SIZE
        ) 
        for _i in range(6)
    )

    charging_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'prop', 'charging-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(6)
    )

    firewall_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'prop', 'firewall-{:02d}.png'.format(_i+1))),
            int(Const.PLAYER_HEIGHT*1.2), int(Const.PLAYER_HEIGHT*1.2)
        )
        for _i in range(4)
    )

    format_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'prop', 'format-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(6)
    )

    get_prop_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'prop', 'get_prop-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(7)
    )

    directory_occupied_frame = resize_surface(
        load_image(os.path.join(Const.IMAGE_PATH, 'prop', 'prop_directory_occupied.png')),
        Const.ITEM_WIDTH, Const.ITEM_HEIGHT
    )

    @classmethod
    def init_convert(cls):
        cls.keep_item_images = tuple( img.convert_alpha() for img in cls.keep_item_images)
        cls.charging_frames = tuple( frame.convert_alpha() for frame in cls.charging_frames)
        cls.firewall_frames = tuple( frame.convert_alpha() for frame in cls.firewall_frames)
        cls.format_frames = tuple( frame.convert_alpha() for frame in cls.format_frames)
        cls.get_prop_frames = tuple( frame.convert_alpha() for frame in cls.get_prop_frames)
        cls.directory_occupied_frame = cls.directory_occupied_frame.convert_alpha()

    def __init__(self, model, delay_of_frames):
        self.model = model
        self.delay_of_frames = delay_of_frames
        self.quicker_delay_of_frames = delay_of_frames // 2
        self.timer = [0]*4
        self.status = ['standing']*4
        self.atmosphere = [
            {'charge' : -1, 'firewall' : 0, 'format' : -1, 'get_prop':-1},
            {'charge' : -1, 'firewall' : 0, 'format' : -1, 'get_prop':-1},
            {'charge' : -1, 'firewall' : 0, 'format' : -1, 'get_prop':-1},
            {'charge' : -1, 'firewall' : 0, 'format' : -1, 'get_prop':-1},
        ]
        self.player_frames_list = tuple(
            player_frames(Const.PLAYER_COLOR[_i]) for _i in range(4)
        )
    
    def draw(self, screen):
        for (player, player_frame) in zip(self.model.players, self.player_frames_list):
            
            if player.is_invisible():
                continue
            if player.in_folder():
                screen.blit(self.directory_occupied_frame, self.directory_occupied_frame.get_rect(center=player.center))
                continue

            # blood
            pg.draw.rect(screen, Const.HP_BAR_COLOR[1], [player.left, player.top-15, player.rect.width*player.blood/Const.PLAYER_FULL_BLOOD, 5])
            
            # empty hp bar
            pg.draw.rect(screen, Const.HP_BAR_COLOR[0], [player.left, player.top-15, player.rect.width, 5], 2)
            
            # energy
            pg.draw.rect(screen, Const.ENERGY_BAR_COLOR[1], [player.left, player.top-10, player.rect.width*(1-player.special_attack_timer/Const.PLAYER_SPECIAL_ATTACK_TIMER), 5])
            
            # empty energy bar
            pg.draw.rect(screen, Const.ENERGY_BAR_COLOR[0], [player.left, player.top-10, player.rect.width, 5], 2)
            
            # item frame
            # pg.draw.rect(screen, Const.ITEM_BOX_COLOR, [player.left-20, player.top-15, Const.ITEM_BOX_SIZE, Const.ITEM_BOX_SIZE], 2)
            
            # item
            if player.keep_item_type != '':
                screen.blit(self.keep_item_images[Const.SPECIAL_ATTACK_KEEP_TO_NUM[player.keep_item_type]],
                    self.keep_item_images[Const.SPECIAL_ATTACK_KEEP_TO_NUM[player.keep_item_type]].get_rect(topleft=(player.left-20, player.top-15)))
            


            # player itself
            if self.status[player.player_id] == 'special_attack_fireball' and self.timer[player.player_id] < ( len(player_frame.attack_fireball_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    screen.blit(player_frame.attack_fireball_frames[self.frame_index_to_draw],
                        player_frame.attack_fireball_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    screen.blit(player_frame.flipped_attack_fireball_frames[self.frame_index_to_draw],
                        player_frame.flipped_attack_fireball_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue

            if self.status[player.player_id] == 'special_attack_THROW_BUG' and self.timer[player.player_id] < ( len(player_frame.attack_bug_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    screen.blit(player_frame.attack_bug_frames[self.frame_index_to_draw],
                        player_frame.attack_bug_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    screen.blit(player_frame.flipped_attack_bug_frames[self.frame_index_to_draw],
                        player_frame.flipped_attack_bug_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue

            if self.status[player.player_id] == 'special_attack_THROW_COFFEE' and self.timer[player.player_id] < ( len(player_frame.attack_coffee_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    screen.blit(player_frame.attack_coffee_frames[self.frame_index_to_draw],
                        player_frame.attack_coffee_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    screen.blit(player_frame.flipped_attack_coffee_frames[self.frame_index_to_draw],
                        player_frame.flipped_attack_coffee_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue

            if (self.status[player.player_id] == 'special_attack_DOS' or self.status[player.player_id] == 'special_attack_DDOS') and self.timer[player.player_id] < ( len(player_frame.attack_ddos_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    screen.blit(player_frame.attack_ddos_frames[self.frame_index_to_draw],
                        player_frame.attack_ddos_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    screen.blit(player_frame.flipped_attack_ddos_frames[self.frame_index_to_draw],
                        player_frame.flipped_attack_ddos_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue

            if self.status[player.player_id] == 'special_attack_FAN' and self.timer[player.player_id] < ( len(player_frame.attack_fan_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    screen.blit(player_frame.attack_fan_frames[self.frame_index_to_draw],
                        player_frame.attack_fan_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    screen.blit(player_frame.flipped_attack_fan_frames[self.frame_index_to_draw],
                        player_frame.flipped_attack_fan_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue

            if self.status[player.player_id] == 'special_attack_LIGHTNING' and self.timer[player.player_id] < ( len(player_frame.attack_lightning_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    screen.blit(player_frame.attack_lightning_frames[self.frame_index_to_draw],
                        player_frame.attack_fan_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    screen.blit(player_frame.flipped_attack_lightning_frames[self.frame_index_to_draw],
                        player_frame.flipped_attack_lightning_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue

            if self.status[player.player_id] == 'common_attack' and self.timer[player.player_id] < ( len(player_frame.common_attack_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    if player.infection():
                        screen.blit(player_frame.poison_common_attack_frames[self.frame_index_to_draw],
                            player_frame.poison_common_attack_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(player_frame.common_attack_frames[self.frame_index_to_draw],
                            player_frame.common_attack_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    if player.infection():
                        screen.blit(player_frame.flipped_poison_common_attack_frames[self.frame_index_to_draw],
                            player_frame.flipped_poison_common_attack_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(player_frame.flipped_common_attack_frames[self.frame_index_to_draw],
                            player_frame.flipped_common_attack_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue
            
            if self.status[player.player_id] == 'be_attacked' and self.timer[player.player_id] < ( len(player_frame.be_attacked_frames) * self.delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    if player.infection():
                        screen.blit(player_frame.poison_be_attacked_frames[self.frame_index_to_draw],
                            player_frame.poison_be_attacked_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(player_frame.be_attacked_frames[self.frame_index_to_draw],
                            player_frame.be_attacked_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    if player.infection():
                        screen.blit(player_frame.flipped_poison_be_attacked_frames[self.frame_index_to_draw],
                            player_frame.flipped_poison_be_attacked_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(player_frame.flipped_be_attacked_frames[self.frame_index_to_draw],
                            player_frame.flipped_be_attacked_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue
            
            if player.is_standing():
                self.status[player.player_id] = 'standing'
                self.timer[player.player_id] = 0
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    if player.infection():
                        screen.blit(player_frame.poison_standing_frames[0],
                            player_frame.poison_standing_frames[0].get_rect(center=player.center))
                    else:
                        screen.blit(player_frame.standing_frames[0],
                            player_frame.standing_frames[0].get_rect(center=player.center))
                else:
                    if player.infection():
                        screen.blit(player_frame.flipped_poison_standing_frames[0],
                            player_frame.flipped_poison_standing_frames[0].get_rect(center=player.center))
                    else:
                        screen.blit(player_frame.flipped_standing_frames[0],
                            player_frame.flipped_standing_frames[0].get_rect(center=player.center))

            elif player.jump_count > 0:
                if self.status[player.player_id] == 'jump':
                    self.timer[player.player_id] += 1
                else:
                    self.status[player.player_id] = 'jump'
                    self.timer[player.player_id] = 0
                self.frame_index_to_draw = (self.timer[player.player_id] // self.delay_of_frames) % len(player_frame.jump_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    if player.infection():
                        screen.blit(
                            player_frame.poison_jump_frames[self.frame_index_to_draw],
                            player_frame.poison_jump_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(
                            player_frame.jump_frames[self.frame_index_to_draw],
                            player_frame.jump_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    if player.infection():
                        screen.blit(
                            player_frame.flipped_poison_jump_frames[self.frame_index_to_draw],
                            player_frame.flipped_poison_jump_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(
                            player_frame.flipped_jump_frames[self.frame_index_to_draw],
                            player_frame.flipped_jump_frames[self.frame_index_to_draw].get_rect(center=player.center))
            else:
                if self.status[player.player_id] == 'walk':
                    self.timer[player.player_id] += 1
                else:
                    self.status[player.player_id] = 'walk'
                    self.timer[player.player_id] = 0
                self.frame_index_to_draw = (self.timer[player.player_id] // self.delay_of_frames) % len(player_frame.walk_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    if player.infection():
                        screen.blit(
                            player_frame.poison_walk_frames[self.frame_index_to_draw],
                            player_frame.poison_walk_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(
                            player_frame.walk_frames[self.frame_index_to_draw],
                            player_frame.walk_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    if player.infection():
                        screen.blit(
                            player_frame.flipped_poison_walk_frames[self.frame_index_to_draw],
                            player_frame.flipped_poison_walk_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(
                            player_frame.flipped_walk_frames[self.frame_index_to_draw],
                            player_frame.flipped_walk_frames[self.frame_index_to_draw].get_rect(center=player.center))
            
            # atmosphere
            if self.atmosphere[player.player_id]['charge'] >= 0:
                frame_ = self.atmosphere[player.player_id]['charge'] // self.delay_of_frames
                screen.blit(self.charging_frames[frame_],
                    self.charging_frames[frame_].get_rect(center=player.center))
                self.atmosphere[player.player_id]['charge'] += 1
                if self.atmosphere[player.player_id]['charge'] == (len(self.charging_frames) * self.delay_of_frames):
                    self.atmosphere[player.player_id]['charge'] = -1
            
            if self.atmosphere[player.player_id]['format'] >= 0:
                frame_ = self.atmosphere[player.player_id]['format'] // self.delay_of_frames
                screen.blit(self.format_frames[frame_],
                    self.format_frames[frame_].get_rect(center=player.center))
                self.atmosphere[player.player_id]['format'] += 1
                if self.atmosphere[player.player_id]['format'] == (len(self.format_frames) * self.delay_of_frames):
                    self.atmosphere[player.player_id]['format'] = -1

            if self.atmosphere[player.player_id]['get_prop'] >= 0:
                frame_ = self.atmosphere[player.player_id]['get_prop'] // self.delay_of_frames
                screen.blit(self.get_prop_frames[frame_],
                    self.get_prop_frames[frame_].get_rect(center=player.center))
                self.atmosphere[player.player_id]['get_prop'] += 1
                if self.atmosphere[player.player_id]['get_prop'] == (len(self.get_prop_frames) * self.delay_of_frames):
                    self.atmosphere[player.player_id]['get_prop'] = -1

            if player.state['immune'] > 0:
                frame_ = self.atmosphere[player.player_id]['firewall'] // self.delay_of_frames
                screen.blit(self.firewall_frames[frame_],
                    self.firewall_frames[frame_].get_rect(center=player.center))

                if self.atmosphere[player.player_id]['firewall'] > 0:
                    self.atmosphere[player.player_id]['firewall'] += 1

                if self.atmosphere[player.player_id]['firewall'] == (len(self.firewall_frames) * self.delay_of_frames):
                    self.atmosphere[player.player_id]['firewall'] = 0

def init():
    View_players.init_convert()