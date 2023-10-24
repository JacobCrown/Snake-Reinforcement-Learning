from model import Linear_QNet
from agents.agent_iface import AgentInterface


class Agent(AgentInterface):
    MAX_MEMORY = 100_000
    BATCH_SIZE = 1000
    LR = 0.001
    GAMMA = 0.9
    INPUT_DIM = 12
    MODEL = Linear_QNet(INPUT_DIM, 256, 3)

