'''File containig all the constant values'''

import enum
from collections import namedtuple
from pathlib import Path


BLOCK_SIZE = 20

BOARD_BLOCK_WIDTH = 15
BOARD_BLOCK_HEIGHT = 15

BOARD_WIDTH = BOARD_BLOCK_WIDTH * BLOCK_SIZE
BOARD_HEIGHT = BOARD_BLOCK_HEIGHT * BLOCK_SIZE

WINDOW_WIDTH = int(BOARD_WIDTH + 2*BLOCK_SIZE)
WINDOW_HEIGHT = int(BOARD_HEIGHT + 2*BLOCK_SIZE)

SNAKE_COLOR = (0, 240, 0)
APPLE_COLOR = (240, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 240)
BORDER_COLOR = (0, 32, 102)
HEAD_COLOR = (255, 255, 0)

FPS = 30

MODELS_DIRPATH = Path(".models")

Point = namedtuple("Point", ("x", "y"))

class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3