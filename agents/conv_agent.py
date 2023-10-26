import numpy as np
import pygame

import constants as c
from agents.agent_iface import AgentInterface
from models.conv_model import Conv_QNet
from game import Game


class ConvAgent(AgentInterface):
    MAX_MEMORY = 1_000_000
    BATCH_SIZE = 10_000
    LR = 1e-4
    GAMMA = 0.99
    INPUT_DIMS = (1, c.BOARD_BLOCK_WIDTH, c.BOARD_BLOCK_HEIGHT)
    MODEL = Conv_QNet(INPUT_DIMS, 3)
    SAVE_MODEL_NAME = "conv_model.pt"
    LOAD_MODEL = False

    def get_current_state(self, game: Game) -> np.ndarray:
        pixels = pygame.surfarray.array2d(game.board)
        pixels.resize((c.BLOCK_SIZE, c.BLOCK_SIZE), refcheck=False)

        # unsqueeze array for color channel
        arr = pixels.reshape((1, c.BLOCK_SIZE, c.BLOCK_SIZE))
        return arr
