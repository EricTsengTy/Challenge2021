import pygame as pg
import os.path

from View.utils import load_image, resize_surface
import Const


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
        self.timer = [0, 0, 0, 0]
        self.status = ['standing', 'standing', 'standing', 'standing']
        self.hello_world_timer = 0
        self.atmosphere = [
            {'charge' : -1, 'firewall' : 0, 'format' : -1, 'get_prop':-1},
            {'charge' : -1, 'firewall' : 0, 'format' : -1, 'get_prop':-1},
            {'charge' : -1, 'firewall' : 0, 'format' : -1, 'get_prop':-1},
            {'charge' : -1, 'firewall' : 0, 'format' : -1, 'get_prop':-1},
        ]
        self.players = [Player(),Player(),Player(),Player()]
    
    def draw(self, screen):
        for (player, player_frame) in zip(self.model.players, self.players):
            
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

            if player.state['immune'] > 0:
                frame_ = self.atmosphere[player.player_id]['firewall'] // self.delay_of_frames
                screen.blit(self.firewall_frames[frame_],
                    self.firewall_frames[frame_].get_rect(center=player.center))

                if self.atmosphere[player.player_id]['firewall'] > 0:
                    self.atmosphere[player.player_id]['firewall'] += 1

                if self.atmosphere[player.player_id]['firewall'] == (len(self.firewall_frames) * self.delay_of_frames):
                    self.atmosphere[player.player_id]['firewall'] = 0


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
                        screen.blit(player_frame.poison_flipped_common_attack_frames[self.frame_index_to_draw],
                            player_frame.poison_flipped_common_attack_frames[self.frame_index_to_draw].get_rect(center=player.center))
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
                        screen.blit(player_frame.poison_flipped_be_attacked_frames[self.frame_index_to_draw],
                            player_frame.poison_flipped_be_attacked_frames[self.frame_index_to_draw].get_rect(center=player.center))
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
                        screen.blit(player_frame.poison_flipped_standing_frames[0],
                            player_frame.poison_flipped_standing_frames[0].get_rect(center=player.center))
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
                            player_frame.poison_flipped_jump_frames[self.frame_index_to_draw],
                            player_frame.poison_flipped_jump_frames[self.frame_index_to_draw].get_rect(center=player.center))
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
                self.frame_index_to_draw = (self.timer[player.player_id] // self.delay_of_frames) % len(self.walk_frames)
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
                            player_frame.poison_flipped_walk_frames[self.frame_index_to_draw],
                            player_frame.poison_flipped_walk_frames[self.frame_index_to_draw].get_rect(center=player.center))
                    else:
                        screen.blit(
                            player_frame.flipped_walk_frames[self.frame_index_to_draw],
                            player_frame.flipped_walk_frames[self.frame_index_to_draw].get_rect(center=player.center))

def init():
    View_players.init_convert()