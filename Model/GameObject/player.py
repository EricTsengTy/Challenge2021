import Const

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.position = Const.PLAYER_INIT_POSITION[player_id] # a pg.Vector2
        self.horizontal_speed = Const.PLAYER_SPEED
        self.vertical_speed = 0 # negative is up, positive is down
    def move(self, direction: str):
        '''
        Move the player along the direction by its speed.
        Will automatically clip the position so no need to worry out-of-bound moving.
        '''
        # Modify position and velocity of player
        if direction=='jump':
            self.vertical_speed = -Const.PLAYER_JUMP_SPEED
        else:
            self.position += self.horizontal_speed / Const.FPS * Const.DIRECTION_TO_VEC2[direction]
        
        self.clip_position()

    def move_every_tick(self):
        if self.position.y>=400 and self.vertical_speed>0:
            # hit the ground
            self.position.y=400
            self.vertical_speed=0
        else:
            # keep falling
            self.position.y += self.vertical_speed/Const.FPS
            self.vertical_speed += Const.PLAYER_GRAVITY/Const.FPS
        self.clip_position()

    def clip_position(self):
        self.position.x = max(0, min(Const.ARENA_SIZE[0], self.position.x))
        self.position.y = max(0, min(Const.ARENA_SIZE[1], self.position.y))