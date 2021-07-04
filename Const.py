import pygame as pg

# model
FPS = 60 # frame per second
GAME_LENGTH = 30 * FPS

PLAYER_INIT_POSITION = [pg.Vector2(200, 400), pg.Vector2(300, 400), pg.Vector2(400, 400), pg.Vector2(500, 400)]
PLAYER_NUMBER = 4
PLYAER_WIDTH = 40
PLYAER_HEIGHT = 40
PLAYER_SHIFT_SPEED = 100
PLAYER_JUMP_SPEED = 100
PLAYER_GRAVITY = 150
PLAYER_FULL_BLOOD = 1000
PLAYER_COMMON_ATTACK_SIZE = 20 #additional size around player
PLAYER_COMMON_ATTACK_DAMAGE = 10
DIRECTION_TO_VEC2 = {
    'up': pg.Vector2(0, -1),
    'left': pg.Vector2(-1, 0),
    'down': pg.Vector2(0, 1),
    'right': pg.Vector2(1, 0),
}

GROUND_POSITION = [
    (  0, 500, 800, 10),
    (  0, 370, 200, 10),
    (150, 430, 200, 10),
]

ITEM_WIDTH = 30
ITEM_HEIGHT = 30
ITEM_TYPE_LIST=['FAN',
                'LIGHTNING',
                'THROW_COFFEE',
                'THROW_BUG',
                'DOS',
                'DDOS',
                'EXE' ,
                'USB',
                'FIREWARM',
                'GRAPHIC_CARD',
                'FORMAT',
                'FOLDER_UNUSED',
                'CHARGE']


# special attack
ARROW_SPEED = 120
ARROW_RADIUS = 5

DOS_ACTIVE_LIMIT = 10
DOS_DAMAGE = 3
DOS_TIMER = 20

DDOS_ACTIVE_LIMIT = 10
DDOS_DAMAGE = 3
DDOS_TIMER = 20
DDOS_RADIUS = 100

COFFEE_WIDTH = 20
COFFEE_HEIGHT = 20
COFFEE_DAMAGE = 30
COFFEE_GRAVITY = 150

BUG_WIDTH = 20
BUG_HEIGHT = 20
BUG_DAMAGE = 30
BUG_GRAVITY = 150

FIREBALL_RADIUS = 15
FIREBALL_SPEED = 300
FIREBALL_DAMAGE = 30

TORNADO_WIDTH = 32
TORNADO_HEIGHT = 70
TORNADO_SPEED = 280
TORNADO_DAMAGE = 30

LIGHTNING_SPEED = 1100
LIGHTNING_DAMAGE = 30
LIGHTNING_INIT_RANGE = 40 
LIGHTNING_TIME = 25

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
ATTACK_RANGE_COLOR = [pg.Color('lightgreen'), pg.Color('orchid1'), pg.Color('lightcyan'), pg.Color('whitesmoke')]
INVISIBLE_COLOR = pg.Color('gray')
BLOCK_COLOR = pg.Color('white')
ITEM_COLOR = pg.Color("purple")
ARROW_COLOR = pg.Color("red")
COFFEE_COLOR = pg.Color("brown")
BUG_COLOR = pg.Color("DarkOliveGreen")

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
