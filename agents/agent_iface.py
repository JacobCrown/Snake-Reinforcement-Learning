import random
import torch
import numpy as np
from typing import Optional

from model import QTrainer
from constants import MODELS_DIRPATH

def load_model_decorator(func):
    def wrapper(self: "AgentInterface", *args, **kwargs):
        if not self.LOAD_MODEL:
            return func(self, *args, **kwargs)

    return wrapper

class AgentInterface:
    '''Interface for different agent management'''
    
    '''Class variables to be overwritten in child class'''

    # Agent will learn also from prevous examples, thus we will store them in memory
    MAX_MEMORY: Optional[int] = None
    BATCH_SIZE: Optional[int] = None

    # Learning rate
    LR: Optional[float] = None

    # States how many inputs neural network should have
    INPUT_DIM: Optional[int] = None

    # Future reward parameter
    GAMMA: Optional[float] = None

    # NN model
    MODEL = None

    # Name for saving model
    SAVE_MODEL_NAME: Optional[str] = None

    # When you want to start playing from loaded model, set in child class to True
    LOAD_MODEL: bool = False


    def __init__(self):
        self._assert_class_vars_set()

        self.n_games = 0
        self.trainer = QTrainer(self.MODEL, lr=self.LR, gamma=self.GAMMA,
                                batch_size=self.BATCH_SIZE)
        self.mem_cntr = 0

        self.state_memory = np.zeros((self.MAX_MEMORY, self.INPUT_DIM), dtype=np.float32)
        self.new_state_memory = np.zeros((self.MAX_MEMORY, self.INPUT_DIM), dtype=np.float32)
        self.action_memory = np.zeros((self.MAX_MEMORY), dtype=np.int32)
        self.reward_memory = np.zeros((self.MAX_MEMORY), dtype=np.float32)
        self.terminal_memory = np.zeros((self.MAX_MEMORY), dtype=bool)

    def _assert_class_vars_set(self):
        assert isinstance(self.MAX_MEMORY, int)
        assert self.BATCH_SIZE is not None
        assert self.LR is not None
        assert isinstance(self.INPUT_DIM, int)
        assert self.GAMMA is not None
        assert self.MODEL is not None
        assert self.SAVE_MODEL_NAME is not None
        
    @load_model_decorator
    def remember(self, state, action, reward, next_state, game_over):
        idx = self.mem_cntr % self.MAX_MEMORY
        self.state_memory[idx] = state
        self.action_memory[idx] = action
        self.reward_memory[idx] = reward
        self.new_state_memory[idx] = next_state
        self.terminal_memory[idx] = game_over

        self.mem_cntr += 1

    @load_model_decorator
    def train(self):
        if self.mem_cntr < self.BATCH_SIZE:
            return

        max_mem = min(self.mem_cntr, self.MAX_MEMORY)
        batch = np.random.choice(max_mem, self.BATCH_SIZE, replace=False)

        state_batch = torch.tensor(self.state_memory[batch])
        next_state_batch = torch.tensor(self.new_state_memory[batch])
        action_batch = torch.tensor(self.action_memory[batch])
        reward_batch = torch.tensor(self.reward_memory[batch])
        terminal_batch = torch.tensor(self.terminal_memory[batch])

        self.trainer.train_step(state_batch, action_batch, reward_batch, \
                                next_state_batch, terminal_batch)

    def _predict(self, state) -> int:
        state_t = torch.tensor(state, dtype=torch.float32)
        prediction = self.MODEL(state_t.unsqueeze(0))
        return int(torch.argmax(prediction).item())
        

    def get_action(self, state) -> int:
        self.epsilon = -1 if self.LOAD_MODEL else 200 - self.n_games
        if random.randint(0, 200) < self.epsilon:
            return random.randint(0, 2)
        return self._predict(state)
    
    def save_model(self):
        MODELS_DIRPATH.mkdir(exist_ok=True)
        torch.save(self.MODEL.state_dict(), MODELS_DIRPATH / self.SAVE_MODEL_NAME)   

    def load_model(self):
        model_path = MODELS_DIRPATH / self.SAVE_MODEL_NAME
        assert model_path.exists()
        self.MODEL.load_state_dict(torch.load(MODELS_DIRPATH / self.SAVE_MODEL_NAME))