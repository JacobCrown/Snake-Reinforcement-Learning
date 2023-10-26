import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


class DQN_Trainer:
    def __init__(self, model, lr, gamma, batch_size):
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.batch_size = batch_size

    def train_step(self, state, action, reward, next_state, game_over):
        self.optimizer.zero_grad()

        batch_index = np.arange(self.batch_size, dtype=np.int32)

        q_eval = self.model(state)[batch_index, action]
        q_next = self.model(next_state)
        q_next[game_over] = 0.0

        target = reward + self.gamma * torch.max(q_next, dim=1).values
    
        loss = self.criterion(target, q_eval)
        loss.backward()
        self.optimizer.step()
