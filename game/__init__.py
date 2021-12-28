import math
import os.path

from game.runtime import Runtime

BEST_REFRESH_RATE = 60
REFRESH_RATE = BEST_REFRESH_RATE
SPEED_UP = 1
SCREEN_X = 1024
SCREEN_Y = 600
RESOURCES = "resources/"

if os.path.isdir(RESOURCES):
    print("Pickup resources from ", RESOURCES)
else:
    RESOURCES = "./"
    print("Pickup resources from .")

runtime = Runtime()


def nor(x, y):
    len = mylen(x, y)
    return x / len, y / len


def mylen(x, y):
    return math.sqrt(x * x + y * y)
