import numpy as np

import constants as c
from agents.agent_iface import AgentInterface
from models.simple_model import Linear_QNet
from game import Game


class SimpleAgentExtended(AgentInterface):
    MAX_MEMORY = 1_000_000
    BATCH_SIZE = 10_000
    LR = 1e-4
    GAMMA = 0.99
    INPUT_DIMS = (28,)
    MODEL = Linear_QNet(INPUT_DIMS, 64, 3)
    SAVE_MODEL_NAME = "simple_model_extended.pt"
    LOAD_MODEL = False

    def get_current_state(self, game: Game) -> np.ndarray:
        """
        State is going to be represented as distance to the wall, presence of apple
        and presence of the tail in given direction. There will be 8 directions. We
        start from Direction.UP, then UP-RIGHT, then RIGHT, in clock-wise order
        """
        head = game.snake.head
        
        dir_l = int(game.snake.direction == c.Direction.LEFT)
        dir_r = int(game.snake.direction == c.Direction.RIGHT)
        dir_u = int(game.snake.direction == c.Direction.UP)
        dir_d = int(game.snake.direction == c.Direction.DOWN)


        state = [
            # UP
            head.y + 1,
            SimpleAgentExtended._check_for_snake_apple_bitmap_intersection(game, 0, -1),
            SimpleAgentExtended._check_for_snake_tail_bitmap_intersection(game, 0, -1),

            # UP-RIGHT
            min(head.y + 1, c.BOARD_BLOCK_WIDTH - head.x),
            SimpleAgentExtended._check_for_snake_apple_bitmap_intersection(game, 1, -1),
            SimpleAgentExtended._check_for_snake_tail_bitmap_intersection(game, 1, -1),

            # RIGHT
            c.BOARD_BLOCK_WIDTH - head.x,
            SimpleAgentExtended._check_for_snake_apple_bitmap_intersection(game, 1, 0),
            SimpleAgentExtended._check_for_snake_tail_bitmap_intersection(game, 1, 0),

            # RIGHT-DOWN
            min(c.BOARD_BLOCK_HEIGHT - head.y, c.BOARD_BLOCK_WIDTH - head.x),
            SimpleAgentExtended._check_for_snake_apple_bitmap_intersection(game, 1, 1),
            SimpleAgentExtended._check_for_snake_tail_bitmap_intersection(game, 1, 1),

            # DOWN
            c.BOARD_BLOCK_HEIGHT - head.y,
            SimpleAgentExtended._check_for_snake_apple_bitmap_intersection(game, 0, 1),
            SimpleAgentExtended._check_for_snake_tail_bitmap_intersection(game, 0, 1),

            # LEFT-DOWN
            min(c.BOARD_BLOCK_HEIGHT - head.y, head.x + 1),
            SimpleAgentExtended._check_for_snake_apple_bitmap_intersection(game, -1, 1),
            SimpleAgentExtended._check_for_snake_tail_bitmap_intersection(game, -1, 1),

            # LEFT
            head.x + 1,
            SimpleAgentExtended._check_for_snake_apple_bitmap_intersection(game, -1, 0),
            SimpleAgentExtended._check_for_snake_tail_bitmap_intersection(game, -1, 0),

            # LEFT-UP
            min(head.y + 1, head.x + 1),
            SimpleAgentExtended._check_for_snake_apple_bitmap_intersection(game, -1, -1),
            SimpleAgentExtended._check_for_snake_tail_bitmap_intersection(game, -1, -1),

            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            ]

        # print("Current State:")
        # print(state)

        return np.array(state, dtype=np.float32)

    @staticmethod
    def _get_apple_bitmap(game: Game):
        arr = np.zeros((c.BOARD_BLOCK_HEIGHT, c.BOARD_BLOCK_WIDTH))
        apple = game.apple
        arr[apple.y, apple.x] = 1
        return arr

    @staticmethod
    def _get_snake_bitmap(game: Game):
        arr = np.zeros((c.BOARD_BLOCK_HEIGHT, c.BOARD_BLOCK_WIDTH))
        snake = game.snake

        x, y = snake.head
        if x < 0 or y < 0 or x == c.BOARD_BLOCK_WIDTH or y == c.BOARD_BLOCK_HEIGHT:
            return arr

        for x, y in snake.points:
            arr[y, x] = 1
        return arr

    @staticmethod
    def _get_current_direction_bitmap(game: Game, x_step: int, y_step: int):
        arr = np.zeros((c.BOARD_BLOCK_HEIGHT, c.BOARD_BLOCK_WIDTH))

        x, y = game.snake.head
        if x < 0 or y < 0 or x == c.BOARD_BLOCK_WIDTH or y == c.BOARD_BLOCK_HEIGHT:
            return arr

        if x_step == 1:
            x_range_end = c.BOARD_BLOCK_WIDTH - x 
        elif x_step == 0:
            x_range_end = c.BOARD_BLOCK_WIDTH
        else:
            x_range_end = x + 1
            
        if y_step == 1:
            y_range_end = c.BOARD_BLOCK_HEIGHT - y 
        elif y_step == 0:
            y_range_end = c.BOARD_BLOCK_HEIGHT
        else:
            y_range_end = y + 1

        xs = [x + x_step * i for i in range(1, x_range_end)]
        ys = [y + y_step * i for i in range(1, y_range_end)]

        # print(f"{x=}")
        # print(f"{y=}")
        # print(f"{x_range_end=}")
        # print(f"{y_range_end=}")
        # print(f"X step {x_step}, Y step {y_step}")
        # print(f"{xs=}")
        # print(f"{ys=}")
        # print()

        try:
            xs, ys = zip(*zip(xs, ys))
        except ValueError:
            return arr
        arr[ys, xs] = 1
        return arr

    @staticmethod
    def _check_for_snake_tail_bitmap_intersection(game, x_step: int, y_step: int) -> int:
        bm = SimpleAgentExtended._get_current_direction_bitmap(game, x_step, y_step)
        bmp2 = SimpleAgentExtended._get_snake_bitmap(game)
        # breakpoint()
        la = np.logical_and(bm, bmp2)
        ab = np.any(la)
        return int(ab)
        
    @staticmethod
    def _check_for_snake_apple_bitmap_intersection(game, x_step: int, y_step: int) -> int:
        bmp1 = SimpleAgentExtended._get_current_direction_bitmap(game, x_step, y_step)
        bmp2 = SimpleAgentExtended._get_apple_bitmap(game)
        la = np.logical_and(bmp1, bmp2)
        ab = np.any(la)
        return int(ab)
