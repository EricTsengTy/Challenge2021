import pygame as pg

# model
FPS = 60 # frame per second
GAME_LENGTH = 30 * FPS
PLAYER_INIT_POSITION = [pg.Vector2(200, 400), pg.Vector2(300, 400), pg.Vector2(400, 400), pg.Vector2(500, 400)]
PLAYER_NUMBER = 4
PLYAER_WIDTH = 40
PLYAER_HEIGHT = 40
PLAYER_SPEED = 100
PLAYER_JUMP_SPEED = 100
PLAYER_GRAVITY = 150

DIRECTION_TO_VEC2 = {
    'up': pg.Vector2(0, -1),
    'left': pg.Vector2(-1, 0),
    'down': pg.Vector2(0, 1),
    'right': pg.Vector2(1, 0),
}

BLOCK_POSITION = [
    (  0, 500, 800, 10),
    (  0, 370, 200, 10),
    (150, 430, 200, 10),
]

# State machine constants
STATE_POP = 0 # for convenience, not really a state which we can be in
STATE_MENU = 1
STATE_PLAY = 2
STATE_STOP = 3 # not implemented yet
STATE_ENDGAME = 4


# view
WINDOW_CAPTION = 'Challenge 2020 Homework'
WINDOW_SIZE = (800, 800)
ARENA_SIZE = (800, 800)
BACKGROUND_COLOR = pg.Color('black')
PLAYER_COLOR = [pg.Color('green'), pg.Color('magenta'), pg.Color('cyan'), pg.Color('white')]
BLOCK_COLOR = pg.Color('white')

# controller
PLAYER_MOVE_KEYS = {
    pg.K_w: (0, 'jump'),
    pg.K_a: (0, 'left'),
    pg.K_d: (0, 'right'),
    pg.K_t: (1, 'jump'),
    pg.K_f: (1, 'left'),
    pg.K_h: (1, 'right'),
    pg.K_i: (2, 'jump'),
    pg.K_j: (2, 'left'),  
    pg.K_l: (2, 'right'),
    pg.K_UP: (3, 'jump'),
    pg.K_LEFT: (3, 'left'),
    pg.K_RIGHT: (3, 'right')
}

PLAYER_ATTACK_KEYS = {
    pg.K_s: (0, 'attack'),
    pg.K_g: (1, 'attack'),
    pg.K_k: (2, 'attack'),
    pg.K_DOWN: (3, 'attack')
}

PLAYER_SPECIAL_ATTACK_KEYS = {
    pg.K_q: (0, 'special_attack'),
    pg.K_r: (1, 'special_attack'),
    pg.K_u: (2, 'special_attack'),
    pg.K_RSHIFT: (3, 'special_attack'),
}
