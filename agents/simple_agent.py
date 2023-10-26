import numpy as np

import constants as c
from agents.agent_iface import AgentInterface
from models.simple_model import Linear_QNet
from game import Game



class SimpleAgent(AgentInterface):
    MAX_MEMORY = 1_000_000
    BATCH_SIZE = 10_000
    LR = 1e-4
    GAMMA = 0.99
    INPUT_DIM = 11
    MODEL = Linear_QNet(INPUT_DIM, 512, 3)
    SAVE_MODEL_NAME = "simple_model.pt"
    LOAD_MODEL = True

    def get_current_state(self, game: Game) -> np.ndarray:
        head = game.snake.head
        point_l = c.Point(head.x - 20, head.y)
        point_r = c.Point(head.x + 20, head.y)
        point_u = c.Point(head.x, head.y - 20)
        point_d = c.Point(head.x, head.y + 20)
        
        dir_l = game.snake.direction == c.Direction.LEFT
        dir_r = game.snake.direction == c.Direction.RIGHT
        dir_u = game.snake.direction == c.Direction.UP
        dir_d = game.snake.direction == c.Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.snake.is_collision(point_r)) or 
            (dir_l and game.snake.is_collision(point_l)) or 
            (dir_u and game.snake.is_collision(point_u)) or 
            (dir_d and game.snake.is_collision(point_d)),

            # Danger right
            (dir_u and game.snake.is_collision(point_r)) or 
            (dir_d and game.snake.is_collision(point_l)) or 
            (dir_l and game.snake.is_collision(point_u)) or 
            (dir_r and game.snake.is_collision(point_d)),

            # Danger left
            (dir_d and game.snake.is_collision(point_r)) or 
            (dir_u and game.snake.is_collision(point_l)) or 
            (dir_r and game.snake.is_collision(point_u)) or 
            (dir_l and game.snake.is_collision(point_d)),
            
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

