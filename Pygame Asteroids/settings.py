
from os import path
import pygame as py
vec = py.math.Vector2

# constant variables
WIDTH = 960
HEIGHT = 544
FPS = 60
TITLE = "Assteroids"
BGCOLOUR = (0,0,0)
TILESIZE = 32

PLAYER_ACC = 0.15
PLAYER_FRICTION = -0.009
ROT_SPEED = 300
SLOW_TURNING = 20

BULLET_SPEED = 500
BULLET_LIFE = 2000
BULLET_RATE = 215
BARREL_OFFSET = vec(20, 0)

ASTEROID_VEL = 0.4
BASE_SCORE = 50

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "img")

PLAYER_IMG = py.image.load(path.join(img_folder, "Player.png"))
BULLET_IMG = py.image.load(path.join(img_folder, "Bullet.png"))
BACKGROUND_IMG = py.image.load(path.join(img_folder, "Background.png"))

SMALL = py.image.load(path.join(img_folder, "small.png"))
MEDIUM = py.image.load(path.join(img_folder, "medium.png"))
LARGE = py.image.load(path.join(img_folder, "large.png"))
