import numpy as np

import constants as c
from agents.agent_iface import AgentInterface
from models.simple_model import Linear_QNet
from game import Game


class SimpleAgent_v2(AgentInterface):
    MAX_MEMORY = 100_000
    BATCH_SIZE = 1000
    LR = 0.001
    GAMMA = 0.99
    INPUT_DIMS = (12,)
    MODEL = Linear_QNet(INPUT_DIMS, 512, 3)
    SAVE_MODEL_NAME = "simple_model_v2.pt"
    LOAD_MODEL = False
    SAVE_MODEL = False

    def get_current_state(self, game: Game) -> np.ndarray:
        head = game.snake.head
        point_l = c.Point(head.x - 1, head.y)
        point_r = c.Point(head.x + 1, head.y)
        point_u = c.Point(head.x, head.y - 1)
        point_d = c.Point(head.x, head.y + 1)
        
        dir_l = game.snake.direction == c.Direction.LEFT
        dir_r = game.snake.direction == c.Direction.RIGHT
        dir_u = game.snake.direction == c.Direction.UP
        dir_d = game.snake.direction == c.Direction.DOWN

        state = [
            game.snake.is_collision(point_r),
            game.snake.is_collision(point_l),
            game.snake.is_collision(point_u),
            game.snake.is_collision(point_d),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            game.apple.x < head.x,  # food left
            game.apple.x > head.x,  # food right
            game.apple.y < head.y,  # food up
            game.apple.y > head.y  # food down
        ]

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

        try:
            xs, ys = zip(*zip(xs, ys))
        except ValueError:
            return arr
        arr[ys, xs] = 1
        return arr

    @staticmethod
    def _check_for_snake_tail_bitmap_intersection(game, x_step: int, y_step: int) -> int:
        bmp1 = SimpleAgent_v2._get_current_direction_bitmap(game, x_step, y_step)
        bmp2 = SimpleAgent_v2._get_snake_bitmap(game)
        la = np.logical_and(bmp1, bmp2)
        ab = np.any(la)
        return int(ab)
        
    @staticmethod
    def _check_for_snake_apple_bitmap_intersection(game, x_step: int, y_step: int) -> int:
        bmp1 = SimpleAgent_v2._get_current_direction_bitmap(game, x_step, y_step)
        bmp2 = SimpleAgent_v2._get_apple_bitmap(game)
        la = np.logical_and(bmp1, bmp2)
        ab = np.any(la)
        return int(ab)
