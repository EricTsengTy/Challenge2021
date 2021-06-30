import pygame
import Const 
class Player(pygame.Rect):
    def __init__(self, player_id):
        pygame.Rect.__init__(self,(Const.PLAYER_INIT_POSITION[player_id].x,
                                   Const.PLAYER_INIT_POSITION[player_id].y,
                                   Const.PLYAER_WIDTH,Const.PLYAER_HEIGHT))
        self.player_id = player_id
        self.max_jump = 2
        self.jump_count = 0
        self.horizontal_speed = Const.PLAYER_SPEED
        self.vertical_speed = 0 # negative is up, positive is down

    def move(self, direction: str):
        '''
        Move the player along the direction by its speed.
        Will automatically clip the position so no need to worry out-of-bound moving.
        '''
        # Modify position and velocity of player
        if direction=='jump':
            # player can jump only if he is falling
            if self.vertical_speed>=0 and self.jump_count < self.max_jump:
                self.jump_count += 1
                self.vertical_speed = -Const.PLAYER_JUMP_SPEED
        else:
            self.center += self.horizontal_speed / Const.FPS * Const.DIRECTION_TO_VEC2[direction]
        self.clip_position()
        

    def move_every_tick(self):
        # keep falling
        self.centery += self.vertical_speed/Const.FPS
        self.vertical_speed += Const.PLAYER_GRAVITY/Const.FPS
        self.clip_position()

    def clip_position(self):
        self.centerx = max(0, min(Const.ARENA_SIZE[0], self.centerx))
        self.centery = max(0, min(Const.ARENA_SIZE[1], self.centery))
    