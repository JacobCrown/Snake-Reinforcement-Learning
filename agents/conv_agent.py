import numpy as np

import constants as c
from agents.agent_iface import AgentInterface
from game import Game



class ConvAgent(AgentInterface):
    MAX_MEMORY = 1_000_000
    BATCH_SIZE = 10_000
    LR = 1e-4
    GAMMA = 0.99
    INPUT_DIM = 11
    SAVE_MODEL_NAME = "conv_model.pt"
    LOAD_MODEL = True

    def get_current_state(self, game: Game) -> np.ndarray:
        pass