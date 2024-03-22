import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 910   # 16 * 32
HEIGHT = 512  # 16 * 32
FPS = 60
TITLE = "Local Tanks"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 150
PLAYER_ROT_SPEED = 180
PLAYER_IMGS = ["tank{0}.png".format(color) for color in ["Black", "Red", "Blue", "Green"]]
TURRET_IMGS = ["turret{0}.png".format(color) for color in ["Black", "Red", "Blue", "Green"]]
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
PLAYER_TURRET_SPEED = 180

# Gun settings
BULLET_IMG = "bulletSilver.png"
BULLET_SPEED = 1500
BULLET_LIFETIME = 1500
BULLET_RATE = 1000
