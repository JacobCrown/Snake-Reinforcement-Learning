import random
import torch
import numpy as np
from typing import Optional

from model import QTrainer


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


    def __init__(self):
        self._assert_class_vars_set()

        self.n_games = 0
        self.gamma = 0.9 
        self.trainer = QTrainer(self.MODEL, lr=self.LR, gamma=self.gamma,
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
        

    def remember(self, state, action, reward, next_state, game_over):
        idx = self.mem_cntr % self.MAX_MEMORY
        self.state_memory[idx] = state
        self.action_memory[idx] = action
        self.reward_memory[idx] = reward
        self.new_state_memory[idx] = next_state
        self.terminal_memory[idx] = game_over

        self.mem_cntr += 1

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

    def get_action(self, state) -> int:
        self.epsilon = 200 - self.n_games
        move = 0 # 0 - left, 1 - straight, 2 - right
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
        else:
            state_t = torch.tensor(state, dtype=torch.float32)
            prediction = self.MODEL(state_t.unsqueeze(0))
            move = int(torch.argmax(prediction).item())

        return move
    