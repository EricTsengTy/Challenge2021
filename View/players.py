import pygame as pg
import os.path

from View.utils import load_image, resize_surface
import Const


class View_players():
    
    standing_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players' , 'standing', 'standing-{:02d}.png'.format(_i+1))), 
            Const.PLAYER_WIDTH,Const.PLAYER_HEIGHT
        )
        for _i in range(1)
    )

    fliped_standing_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in standing_frames
    )

    poison_standing_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players' , 'standing', 'poison_standing-{:02d}.png'.format(_i+1))), 
            Const.PLAYER_WIDTH,Const.PLAYER_HEIGHT
        )
        for _i in range(1)
    )

    poison_fliped_standing_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in poison_standing_frames
    )

    walk_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'right_move', 'right_move-{:02d}.png'.format(_i))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        ) 
        for _i in range(1,9)
    )
    
    fliped_walk_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in walk_frames
    )

    poison_walk_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'right_move', 'poison_right_move-{:02d}.png'.format(_i))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        ) 
        for _i in range(1,9)
    )
    
    poison_fliped_walk_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in poison_walk_frames
    )

    jump_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'jump_drop', 'jump_drop-{:02d}.png'.format(_i))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(1,14)
    )

    fliped_jump_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in jump_frames
    )

    poison_jump_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'jump_drop', 'poison_jump_drop-{:02d}.png'.format(_i))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(1,14)
    )

    poison_fliped_jump_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in poison_jump_frames
    )

    keep_item_images = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'special_attack_keep', Const.SPECIAL_ATTACK_KEEP_PICS[_i])),
            Const.ITEM_BOX_SIZE, Const.ITEM_BOX_SIZE
        ) 
        for _i in range(6)
    )

    common_attack_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'physical_atk', 'physical_atk-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(13)
    )

    fliped_common_attack_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in common_attack_frames
    )

    poison_common_attack_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'physical_atk', 'poison_physical_atk-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(13)
    )

    poison_fliped_common_attack_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in poison_common_attack_frames
    )

    be_attacked_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'be_attacked', 'be_attacked-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(9)
    )

    fliped_be_attacked_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in be_attacked_frames
    )

    poison_be_attacked_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'be_attacked', 'poison_be_attacked-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(9)
    )

    poison_fliped_be_attacked_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in poison_be_attacked_frames
    )

    attack_fireball_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'special_atk', 'fire_ball-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(13)
    )

    fliped_attack_fireball_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in attack_fireball_frames
    )

    attack_bug_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'special_atk', 'bug-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(9)
    )

    fliped_attack_bug_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in attack_bug_frames
    )

    attack_coffee_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'special_atk', 'coffee-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(9)
    )

    fliped_attack_coffee_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in attack_coffee_frames
    )

    attack_ddos_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'special_atk', 'DDOS-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(13)
    )

    fliped_attack_ddos_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in attack_ddos_frames
    )

    attack_fan_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'special_atk', 'fan-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(13)
    )

    fliped_attack_fan_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in attack_fan_frames
    )

    attack_lightning_frames = tuple(
        resize_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'players', 'special_atk', 'lightning-{:02d}.png'.format(_i+1))),
            Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT
        )
        for _i in range(13)
    )

    fliped_attack_lightning_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in attack_lightning_frames
    )

    '''
    hello_world_frames = tuple(
        scale_surface(
            load_image(os.path.join(Const.IMAGE_PATH, 'hello_world', f'hello_world3_{_i+1}.png')), 1
        )
        for _i in range(4)
    )

    fliped_hello_world_frames = tuple(
        pg.transform.flip(_frame, True, False) for _frame in hello_world_frames
    )
    '''

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
        cls.standing_frames = tuple( frame.convert_alpha() for frame in cls.standing_frames)
        cls.fliped_standing_frames = tuple( frame.convert_alpha() for frame in cls.fliped_standing_frames)
        cls.walk_frames = tuple( frame.convert_alpha() for frame in cls.walk_frames)
        cls.fliped_walk_frames = tuple( frame.convert_alpha() for frame in cls.fliped_walk_frames)
        cls.jump_frames = tuple( frame.convert_alpha() for frame in cls.jump_frames)
        cls.fliped_jump_frames = tuple( frame.convert_alpha() for frame in cls.fliped_jump_frames)
        cls.keep_item_images = tuple( img.convert_alpha() for img in cls.keep_item_images)
        cls.common_attack_frames = tuple( frame.convert_alpha() for frame in cls.common_attack_frames)
        cls.fliped_common_attack_frames = tuple( frame.convert_alpha() for frame in cls.fliped_common_attack_frames)
        cls.be_attacked_frames = tuple( frame.convert_alpha() for frame in cls.be_attacked_frames)
        cls.fliped_be_attacked_frames = tuple( frame.convert_alpha() for frame in cls.fliped_be_attacked_frames)
        cls.attack_fireball_frames = tuple( frame.convert_alpha() for frame in cls.attack_fireball_frames)
        cls.fliped_attack_fireball_frames = tuple( frame.convert_alpha() for frame in cls.fliped_attack_fireball_frames)
        cls.attack_bug_frames = tuple( frame.convert_alpha() for frame in cls.attack_bug_frames)
        cls.fliped_attack_bug_frames = tuple( frame.convert_alpha() for frame in cls.fliped_attack_bug_frames)
        cls.attack_coffee_frames = tuple( frame.convert_alpha() for frame in cls.attack_coffee_frames)
        cls.fliped_attack_coffee_frames = tuple( frame.convert_alpha() for frame in cls.fliped_attack_coffee_frames)
        cls.attack_ddos_frames = tuple( frame.convert_alpha() for frame in cls.attack_ddos_frames)
        cls.fliped_attack_ddos_frames = tuple( frame.convert_alpha() for frame in cls.fliped_attack_ddos_frames)
        cls.attack_fan_frames = tuple( frame.convert_alpha() for frame in cls.attack_fan_frames)
        cls.fliped_attack_fan_frames = tuple( frame.convert_alpha() for frame in cls.fliped_attack_fan_frames)
        cls.attack_lightning_frames = tuple( frame.convert_alpha() for frame in cls.attack_lightning_frames)
        cls.fliped_attack_lightning_frames = tuple( frame.convert_alpha() for frame in cls.fliped_attack_lightning_frames)
        cls.poison_standing_frames = tuple( frame.convert_alpha() for frame in cls.poison_standing_frames)
        cls.poison_fliped_standing_frames = tuple( frame.convert_alpha() for frame in cls.poison_fliped_standing_frames)
        cls.poison_walk_frames = tuple( frame.convert_alpha() for frame in cls.poison_walk_frames)
        cls.poison_fliped_walk_frames = tuple( frame.convert_alpha() for frame in cls.poison_fliped_walk_frames)
        cls.poison_jump_frames = tuple( frame.convert_alpha() for frame in cls.poison_jump_frames)
        cls.poison_fliped_jump_frames = tuple( frame.convert_alpha() for frame in cls.poison_fliped_jump_frames)
        cls.poison_common_attack_frames = tuple( frame.convert_alpha() for frame in cls.poison_common_attack_frames)
        cls.poison_fliped_common_attack_frames = tuple( frame.convert_alpha() for frame in cls.poison_fliped_common_attack_frames)
        cls.poison_be_attacked_frames = tuple( frame.convert_alpha() for frame in cls.poison_be_attacked_frames)
        cls.poison_fliped_be_attacked_frames = tuple( frame.convert_alpha() for frame in cls.poison_fliped_be_attacked_frames)
        # cls.hello_world_frames = tuple( frame.convert_alpha() for frame in cls.hello_world_frames)
        # cls.fliped_hello_world_frames = tuple( frame.convert_alpha() for frame in cls.fliped_hello_world_frames)
        cls.charging_frames = tuple( frame.convert_alpha() for frame in cls.charging_frames)
        cls.firewall_frames = tuple( frame.convert_alpha() for frame in cls.firewall_frames)
        cls.format_frames = tuple( frame.convert_alpha() for frame in cls.format_frames)
        cls.get_prop_frames = tuple( frame.convert_alpha() for frame in cls.get_prop_frames)
        cls.directory_occupied_frame = cls.directory_occupied_frame.convert_alpha()

    def __init__(self, model, delay_of_frames):
        self.model = model
        self.delay_of_frames = delay_of_frames
        self.quicker_delay_of_frames = delay_of_frames // 2
        self.timer = [0, 0, 0, 0]
        self.status = ['standing', 'standing', 'standing', 'standing']
        self.hello_world_timer = 0
        self.atmosphere = [
            {'charge' : -1, 'firewall' : 0, 'format' : -1, 'get_prop':-1},
            {'charge' : -1, 'firewall' : 0, 'format' : -1, 'get_prop':-1},
            {'charge' : -1, 'firewall' : 0, 'format' : -1, 'get_prop':-1},
            {'charge' : -1, 'firewall' : 0, 'format' : -1, 'get_prop':-1},
        ]
    
    def draw(self, screen):
        for player in self.model.players:
            
            # hello world type 3
            if self.hello_world_timer > 0:
                pass
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

            # player itself
            if self.status[player.player_id] == 'special_attack_fireball' and self.timer[player.player_id] < ( len(self.attack_fireball_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    screen.blit(self.attack_fireball_frames[self.frame_index_to_draw],
                        self.attack_fireball_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    screen.blit(self.fliped_attack_fireball_frames[self.frame_index_to_draw],
                        self.fliped_attack_fireball_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue

            if self.status[player.player_id] == 'special_attack_THROW_BUG' and self.timer[player.player_id] < ( len(self.attack_bug_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    screen.blit(self.attack_bug_frames[self.frame_index_to_draw],
                        self.attack_bug_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    screen.blit(self.fliped_attack_bug_frames[self.frame_index_to_draw],
                        self.fliped_attack_bug_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue

            if self.status[player.player_id] == 'special_attack_THROW_COFFEE' and self.timer[player.player_id] < ( len(self.attack_coffee_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    screen.blit(self.attack_coffee_frames[self.frame_index_to_draw],
                        self.attack_coffee_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    screen.blit(self.fliped_attack_coffee_frames[self.frame_index_to_draw],
                        self.fliped_attack_coffee_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue

            if (self.status[player.player_id] == 'special_attack_DOS' or self.status[player.player_id] == 'special_attack_DDOS') and self.timer[player.player_id] < ( len(self.attack_ddos_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    screen.blit(self.attack_ddos_frames[self.frame_index_to_draw],
                        self.attack_ddos_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    screen.blit(self.fliped_attack_ddos_frames[self.frame_index_to_draw],
                        self.fliped_attack_ddos_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue

            if self.status[player.player_id] == 'special_attack_FAN' and self.timer[player.player_id] < ( len(self.attack_fan_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    screen.blit(self.attack_fan_frames[self.frame_index_to_draw],
                        self.attack_fan_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    screen.blit(self.fliped_attack_fan_frames[self.frame_index_to_draw],
                        self.fliped_attack_fan_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue

            if self.status[player.player_id] == 'special_attack_LIGHTNING' and self.timer[player.player_id] < ( len(self.attack_lightning_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    screen.blit(self.attack_lightning_frames[self.frame_index_to_draw],
                        self.attack_fan_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    screen.blit(self.fliped_attack_lightning_frames[self.frame_index_to_draw],
                        self.fliped_attack_lightning_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue

            if self.status[player.player_id] == 'common_attack' and self.timer[player.player_id] < ( len(self.common_attack_frames) * self.quicker_delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.quicker_delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    if player.infection():
                        screen.blit(self.poison_common_attack_frames[self.frame_index_to_draw],
                            self.poison_common_attack_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(self.common_attack_frames[self.frame_index_to_draw],
                            self.common_attack_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    if player.infection():
                        screen.blit(self.poison_fliped_common_attack_frames[self.frame_index_to_draw],
                            self.poison_fliped_common_attack_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(self.fliped_common_attack_frames[self.frame_index_to_draw],
                            self.fliped_common_attack_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue
            
            if self.status[player.player_id] == 'be_attacked' and self.timer[player.player_id] < ( len(self.be_attacked_frames) * self.delay_of_frames):
                
                self.frame_index_to_draw = (self.timer[player.player_id] // self.delay_of_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    if player.infection():
                        screen.blit(self.poison_be_attacked_frames[self.frame_index_to_draw],
                            self.poison_be_attacked_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(self.be_attacked_frames[self.frame_index_to_draw],
                            self.be_attacked_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    if player.infection():
                        screen.blit(self.poison_fliped_be_attacked_frames[self.frame_index_to_draw],
                            self.poison_fliped_be_attacked_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(self.fliped_be_attacked_frames[self.frame_index_to_draw],
                            self.fliped_be_attacked_frames[self.frame_index_to_draw].get_rect(center=player.center))
                self.timer[player.player_id] += 1
                continue
            
            if player.is_standing():
                self.status[player.player_id] = 'standing'
                self.timer[player.player_id] = 0
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    if player.infection():
                        screen.blit(self.poison_standing_frames[0],
                            self.poison_standing_frames[0].get_rect(center=player.center))
                    else:
                        screen.blit(self.standing_frames[0],
                            self.standing_frames[0].get_rect(center=player.center))
                else:
                    if player.infection():
                        screen.blit(self.poison_fliped_standing_frames[0],
                            self.poison_fliped_standing_frames[0].get_rect(center=player.center))
                    else:
                        screen.blit(self.fliped_standing_frames[0],
                            self.fliped_standing_frames[0].get_rect(center=player.center))

            elif player.jump_count > 0:
                if self.status[player.player_id] == 'jump':
                    self.timer[player.player_id] += 1
                else:
                    self.status[player.player_id] = 'jump'
                    self.timer[player.player_id] = 0
                self.frame_index_to_draw = (self.timer[player.player_id] // self.delay_of_frames) % len(self.jump_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    if player.infection():
                        screen.blit(
                            self.poison_jump_frames[self.frame_index_to_draw],
                            self.poison_jump_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(
                            self.jump_frames[self.frame_index_to_draw],
                            self.jump_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    if player.infection():
                        screen.blit(
                            self.poison_fliped_jump_frames[self.frame_index_to_draw],
                            self.poison_fliped_jump_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(
                            self.fliped_jump_frames[self.frame_index_to_draw],
                            self.fliped_jump_frames[self.frame_index_to_draw].get_rect(center=player.center))
            else:
                if self.status[player.player_id] == 'walk':
                    self.timer[player.player_id] += 1
                else:
                    self.status[player.player_id] = 'walk'
                    self.timer[player.player_id] = 0
                self.frame_index_to_draw = (self.timer[player.player_id] // self.delay_of_frames) % len(self.walk_frames)
                if player.face == Const.DIRECTION_TO_VEC2['right']:
                    if player.infection():
                        screen.blit(
                            self.poison_walk_frames[self.frame_index_to_draw],
                            self.poison_walk_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(
                            self.walk_frames[self.frame_index_to_draw],
                            self.walk_frames[self.frame_index_to_draw].get_rect(center=player.center))
                else:
                    if player.infection():
                        screen.blit(
                            self.poison_fliped_walk_frames[self.frame_index_to_draw],
                            self.poison_fliped_walk_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(
                            self.fliped_walk_frames[self.frame_index_to_draw],
                            self.fliped_walk_frames[self.frame_index_to_draw].get_rect(center=player.center))

def init():
    View_players.init_convert()