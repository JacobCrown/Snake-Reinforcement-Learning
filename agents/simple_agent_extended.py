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
    INPUT_DIMS = (11,)
    MODEL = Linear_QNet(INPUT_DIMS, 512, 3)
    SAVE_MODEL_NAME = "simple_model_extended.pt"
    LOAD_MODEL = False

    def get_current_state(self, game: Game) -> np.ndarray:
        pass