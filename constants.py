'''File containig all the constant values'''

import enum
from collections import namedtuple


WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200
BLOCK_SIZE = 20
SNAKE_COLOR = (0, 240, 0)
APPLE_COLOR = (240, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 240)
FPS = 15

Point = namedtuple("Point", ("x", "y"))

class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3