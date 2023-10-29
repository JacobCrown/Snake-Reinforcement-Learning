import numpy as np

import constants as c
from agents.agent_iface import AgentInterface
from models.simple_model import Linear_QNet
from game import Game


class Agent(AgentInterface):
    MAX_MEMORY = 10_000
    BATCH_SIZE = 100
    LR = 1e-4
    GAMMA = 0.99
    INPUT_DIMS = (11,)
    MODEL = Linear_QNet(INPUT_DIMS, 512, 3)
    SAVE_MODEL_NAME = "little_more_robust_model.pt"
    LOAD_MODEL = False

    def get_current_state(self, game: Game) -> np.ndarray:
        head = game.snake.head
        
        dir_l = game.snake.direction == c.Direction.LEFT
        dir_r = game.snake.direction == c.Direction.RIGHT
        dir_u = game.snake.direction == c.Direction.UP
        dir_d = game.snake.direction == c.Direction.DOWN

        state = [
            # 1. Distance to the wall
            # 2. Is there an apple? (1/0)
            # 3. Is there a tail? (1/0)

            # Direction up
            
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            ]

        return np.array(state, dtype=np.float32)


