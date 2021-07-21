import pygame as pg
import os.path

# model
FPS = 60 # frame per second
GAME_LENGTH = 60 * FPS

PLAYER_INIT_POSITION = [pg.Vector2(50, 160), pg.Vector2(500, 0), pg.Vector2(800, 360), pg.Vector2(1000, 160)]
PLAYER_NUMBER = 4
PLAYER_WIDTH = 90
PLAYER_HEIGHT = 120
PLAYER_SHIFT_SPEED = 150
PLAYER_JUMP_SPEED = 200
PLAYER_SPEED_ADJUST = 0.5
PLAYER_GRAVITY = 200
PLAYER_FULL_BLOOD = 1000
PLAYER_COMMON_ATTACK_SIZE = 20 #additional size around player
PLAYER_COMMON_ATTACK_DAMAGE = 10
PLAYER_COMMON_ATTACK_DAMAGE_ADJUST = 1.5
PLAYER_SPECIAL_ATTACK_TIMER = 1 * FPS
PLAYER_COMMON_ATTACK_TIMER = 0.5 * FPS
PLAYER_SPECIAL_ATTACK_DELAY = 0.5 * FPS

SCORE_KILL_OTHER = 500
SCORE_NEVER_DIE = 1000
SCORE_HELLO_WORLD = 300

#item effect
ENERGY_MULTIPLE = 2 # multiple of accumulate energy speed affected by video card

DIRECTION_TO_VEC2 = {
    'up': pg.Vector2(0, -1),
    'left': pg.Vector2(-1, 0),
    'down': pg.Vector2(0, 1),
    'right': pg.Vector2(1, 0),
}

#(left, top, width, height)
GROUND_POSITION = [
    (  450, 160, 480, 40),
    (  0, 360, 400, 40),
    (  800, 360, 400, 40),
    (  200, 560, 720, 40),
    (  0, 760, 1200, 40)
]
GROUND_SIZE = 40

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
MAX_ITEM_NUMBER = 10

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
LIGHTNING_SIZE = 20

# state time
INFECTED_TIME = 3 * FPS
INFECTED_COMMON_ATTACK_TIME = 10 * FPS
INVISIBLE_TIME = int(0.5 * FPS)
IN_FOLDER_TIME = 3 * FPS
SLOW_DOWN_TIME = 3 * FPS
BROKEN_TIME_COFFEE = 3 * FPS
BROKEN_TIME_BUG = 3 * FPS
FIREWALL_TIME = 10 * FPS
GRAPHIC_CARD_TIME = 3 * FPS

# State machine constants
STATE_POP = 0 # for convenience, not really a state which we can be in
STATE_MENU = 1
STATE_PLAY = 2
STATE_STOP = 3 # not implemented yet
STATE_ENDGAME = 4
STATE_TUTORIAL = 5

# Path
IMAGE_PATH = os.path.join('View', 'assets')

# Images

SPECIAL_ATTACK_KEEP_PICS = [
    'prop_bug.png', 'prop_coffee.png',
    'prop_ddos.png', 'prop_dos.png',
    'prop_fan.png', 'prop_lightning.png',
    ]
SPECIAL_ATTACK_KEEP_TO_NUM = {
    'THROW_BUG': 0, 'THROW_COFFEE': 1, 'DDOS': 2, 'DOS': 3, 'FAN': 4, 'LIGHTNING': 5
}

PROP_PICS = [
    'prop_fan.png', 'prop_lightning.png', 'prop_coffee.png', 'prop_bug.png', 
    'prop_dos.png', 'prop_ddos.png', 'prop_hello_world.png', 'prop_usb.png', 'prop_firewall.png', 
    'prop_graphic_card.png', 'prop_format.png', 'prop_directory.png', 'prop_charge_line.png', 'prop.png'       
]
# view
WINDOW_CAPTION = 'Challenge 2021'
WINDOW_SIZE = (1200, 800)
ARENA_SIZE = (1200, 800)
BACKGROUND_COLOR = pg.Color('black')
PLAYER_COLOR = [pg.Color('green'), pg.Color('magenta'), pg.Color('cyan'), pg.Color('white')]
PLAYER_COLOR_DRAWER = True
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
    pg.K_a: (0, 'left'),
    pg.K_d: (0, 'right'),
    pg.K_f: (1, 'left'),
    pg.K_h: (1, 'right'),
    pg.K_j: (2, 'left'),  
    pg.K_l: (2, 'right'),
    pg.K_LEFT: (3, 'left'),
    pg.K_RIGHT: (3, 'right')
}

PLAYER_JUMP_KEYS = {
    pg.K_w: (0, 'jump'),
    pg.K_t: (1, 'jump'),
    pg.K_i: (2, 'jump'),
    pg.K_UP: (3, 'jump'),
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
