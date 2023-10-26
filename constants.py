'''File containig all the constant values'''

import enum
from collections import namedtuple
from pathlib import Path

BOARD_WIDTH = 20
BOARD_HEIGHT = 20

BLOCK_SIZE = 20

WINDOW_WIDTH = int(BOARD_WIDTH * BLOCK_SIZE)
WINDOW_HEIGHT = int(BOARD_HEIGHT * BLOCK_SIZE)

SNAKE_COLOR = (0, 240, 0)
APPLE_COLOR = (240, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 240)

FPS = 20

MODELS_DIRPATH = Path(".models")

Point = namedtuple("Point", ("x", "y"))

class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3