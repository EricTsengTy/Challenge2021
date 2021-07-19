import pygame as pg

# model
FPS = 60 # frame per second
GAME_LENGTH = 30 * FPS
PLAYER_INIT_POSITION = [pg.Vector2(200, 400), pg.Vector2(600, 400)]
PLAYER_RADIUS = 75
SPEED_ATTACK = 100
SPEED_DEFENSE = 70
DIRECTION_TO_VEC2 = {
    'up': pg.Vector2(0, -1),
    'left': pg.Vector2(-1, 0),
    'down': pg.Vector2(0, 1),
    'right': pg.Vector2(1, 0),
}


# State machine constants
STATE_POP = 0 # for convenience, not really a state which we can be in
STATE_MENU = 1
STATE_PLAY = 2
STATE_STOP = 3 # not implemented yet
STATE_ENDGAME = 4
STATE_TUTORIAL = 5


# view
WINDOW_CAPTION = 'Challenge 2020 Homework'
WINDOW_SIZE = (800, 800)
ARENA_SIZE = (800, 800)
BACKGROUND_COLOR = pg.Color('black')
PLAYER_COLOR = [pg.Color('green'), pg.Color('magenta')]


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