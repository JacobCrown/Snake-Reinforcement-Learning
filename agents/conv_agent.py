import numpy as np

import constants as c
from agents.agent_iface import AgentInterface
from models.conv_model import Conv_QNet
from game import Game


class ConvAgent(AgentInterface):
    MAX_MEMORY = 1_000_000
    BATCH_SIZE = 10_000
    LR = 1e-4
    GAMMA = 0.99
    INPUT_DIMS = (3, c.BOARD_BLOCK_WIDTH + 2, c.BOARD_BLOCK_HEIGHT + 2)
    MODEL = Conv_QNet(INPUT_DIMS, 3)
    SAVE_MODEL_NAME = "conv_model.pt"
    LOAD_MODEL = False

    def get_current_state(self, game: Game) -> np.ndarray:
        pixels = game.get_board_pixels()
        return pixels
