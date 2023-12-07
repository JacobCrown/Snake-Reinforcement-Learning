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
            
            # Food location 
            game.apple.x < head.x,  # food left
            game.apple.x > head.x,  # food right
            game.apple.y < head.y,  # food up
            game.apple.y > head.y  # food down
        ]

        return np.array(state, dtype=np.float32)

