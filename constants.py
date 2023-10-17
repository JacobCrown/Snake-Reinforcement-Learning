'''File containig all the constant values'''

import enum


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BLOCK_SIZE = 20
SNAKE_COLOR = (0, 240, 0)

class Direction(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3