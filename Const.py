import pygame as pg
import os.path

# model
FPS = 60 # frame per second
GAME_LENGTH = 30 * FPS

PLAYER_INIT_POSITION = [pg.Vector2(200, 400), pg.Vector2(300, 400), pg.Vector2(400, 400), pg.Vector2(500, 400)]
PLAYER_NUMBER = 4
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 40
PLAYER_SHIFT_SPEED = 100
PLAYER_JUMP_SPEED = 100
PLAYER_SPEED_ADJUST_RATIO = 0.5
PLAYER_GRAVITY = 150
PLAYER_FULL_BLOOD = 1000
PLAYER_COMMON_ATTACK_SIZE = 20 #additional size around player
PLAYER_COMMON_ATTACK_DAMAGE = 10
PLAYER_INFECTED_COMMON_ATTACK_DAMAGE = 15

#entity
ARROW_TYPE = 15
ARROW_SPEED = 120
ARROW_RADIUS = 5

DOS_ACTIVE_LIMIT = 10
DOS_DAMAGE = 3
DOS_TIMER = 20

DDOS_ACTIVE_LIMIT = 4
DDOS_RANGE = 80
DDOS_DAMAGE = 2
DDOS_TIMER = 20

COFFEE_WIDTH = 20
COFFEE_HEIGHT = 20
COFFEE_SPEED = {"right": pg.Vector2(100, -150), "left": pg.Vector2(-100, -150)}
COFFEE_ACCELERATE = 150
COFFEE_DAMAGE = 30

BUG_WIDTH = 20
BUG_HEIGHT = 20
BUG_SPEED = {"right": pg.Vector2(100, -150), "left": pg.Vector2(-100, -150)}
BUG_ACCELERATE = 150
BUG_DAMAGE = 30

#item effect
DAMAGE_MULTIPLE = 2 # multiple of common attack damage affected by USB
SPEED_MULTIPLE = 0.5 # multiple of speed affected by DOS and DDOS
ENERGY_MULTIPLE = 2 # multiple of accumulate energy speed affected by video card

DIRECTION_TO_VEC2 = {
    'up': pg.Vector2(0, -1),
    'left': pg.Vector2(-1, 0),
    'down': pg.Vector2(0, 1),
    'right': pg.Vector2(1, 0),
}

GROUND_POSITION = [
    (  0, 500, 1200, 10),
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
                'FIREWALL',
                'GRAPHIC_CARD',
                'FORMAT',
                'FOLDER_UNUSED',
                'CHARGE']


# special attack
ARROW_SPEED = 120
ARROW_SIZE = 20

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
COFFEE_THROW_SPEED = 120

BUG_WIDTH = 20
BUG_HEIGHT = 20
BUG_DAMAGE = 30
BUG_GRAVITY = 150
BUG_THROW_SPEED = 120

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

# Path
IMAGE_PATH = os.path.join('View', 'assets')

# Images
PLAYER_PICS = [
    'player1_0.png', 'player1_1.png',
    'player2_0.png', 'player2_1.png',
    'player3_0.png', 'player3_1.png',
    'player4_0.png', 'player4_1.png',
    ]
PICS_PER_PLAYER = 2

SPECIAL_ATTACK_KEEP_PICS = [
    'prop_bug.png', 'prop_coffee.png',
    'prop_ddos.png', 'prop_dos.png',
    'prop_fan.png', 'prop_lightning.png',
    ]
SPECIAL_ATTACK_KEEP_TO_NUM = {
    'THROW_BUG': 0, 'THROW_COFFEE': 1, 'DDOS': 2, 'DOS': 3, 'FAN': 4, 'LIGHTNING': 5
}
# view
WINDOW_CAPTION = 'Challenge 2021'
WINDOW_SIZE = (1200, 800)
ARENA_SIZE = (1200, 800)
BACKGROUND_COLOR = pg.Color('black')
PLAYER_COLOR = [pg.Color('green'), pg.Color('magenta'), pg.Color('cyan'), pg.Color('white')]
ATTACK_RANGE_COLOR = [pg.Color('lightgreen'), pg.Color('orchid1'), pg.Color('lightcyan'), pg.Color('whitesmoke')]
INVISIBLE_COLOR = pg.Color('gray')
BLOCK_COLOR = pg.Color('white')
ITEM_COLOR = pg.Color("purple")
ARROW_COLOR = pg.Color("red")
COFFEE_COLOR = pg.Color("brown")
BUG_COLOR = pg.Color("DarkOliveGreen")
HP_BAR_COLOR = [pg.Color('white'), pg.Color('green')]
ENERGY_BAR_COLOR = [pg.Color('white'), pg.Color('orange')]
ITEM_BOX_COLOR = pg.Color('brown')
ITEM_BOX_SIZE = 15
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

GAME_STOP_KEY = pg.K_SPACE
GAME_CONTINUE_KEY = pg.K_RETURN
GAME_RESTART_KEY = pg.K_F5
GAME_FULLSCREEN_KEY = pg.K_F11
