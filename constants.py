'''File containig all the constant values'''

import enum
from collections import namedtuple


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
BLOCK_SIZE = 20
SNAKE_COLOR = (0, 240, 0)
APPLE_COLOR = (240, 0, 0)

Point = namedtuple("Point", ("x", "y"))

class Direction(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3