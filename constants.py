'''File containig all the constant values'''

import enum


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

class Direction(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3