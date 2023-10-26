import torch
import torch.nn as nn
import torch.nn.functional as F


class Conv_QNet(nn.Module):
    def __init__(self, in_dims: (int, int, int), num_actions: int):
        super().__init__()
        in_channels, h, w = in_dims
        self.conv1 = nn.Conv2d(in_channels, 32, kernel_size=3)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(64 * (h-6) * (w-6), 128)  # Adjust the input size if needed
        self.fc2 = nn.Linear(128, num_actions)

    def forward(self, x):
        x = F.leaky_relu(self.conv1(x))
        x = F.leaky_relu(self.conv2(x))
        x = F.leaky_relu(self.conv3(x))
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.fc2(x)
        return x



m = Conv_QNet((1, 20, 20), 3)

t = torch.randn((100, 1, 20, 20))

m(t)