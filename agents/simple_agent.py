from model import Linear_QNet
from agents.agent_iface import AgentInterface


class SimpleAgent(AgentInterface):
    MAX_MEMORY = 1_000_000
    BATCH_SIZE = 10_000
    LR = 1e-4
    GAMMA = 0.99
    INPUT_DIM = 11
    MODEL = Linear_QNet(INPUT_DIM, 512, 3)
    SAVE_MODEL_NAME = "simple_model.pt"
    LOAD_MODEL = True

