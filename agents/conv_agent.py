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
    INPUT_DIMS = (c.BOARD_BLOCK_WIDTH, c.BOARD_BLOCK_HEIGHT)
    MODEL = Conv_QNet(1, 1, c.BLOCK_SIZE, c.BLOCK_SIZE, 0, 3)
    SAVE_MODEL_NAME = "conv_model.pt"
    LOAD_MODEL = False

    def get_current_state(self, game: Game) -> np.ndarray:
        pixels = pygame.surfarray.array3d(game.board)
        pixels.resize((c.BLOCK_SIZE, c.BLOCK_SIZE), refcheck=False)
        return pixels
