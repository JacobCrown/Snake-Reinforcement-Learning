import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.linear3(x)
        return x


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over):
        self.optimizer.zero_grad()

        batch_index = np.arange(state, dtype=np.int32)

        q_eval = self.model(state)[batch_index, action]
        q_next = self.model(next_state)
        q_next[game_over] = 0.0

        target = reward + self.gamma * torch.max(q_next, dim=1)
    
        loss = self.criterion(target, q_eval)
        loss.backward()
        self.optimizer.step()
