import torch.nn as nn
import torch.nn.functional as F


class Conv_QNet(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding, 
                 output_size):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)
        self.flatten = nn.Flatten()
        self.linear = nn.Linear(out_channels, output_size)

    def forward(self, x):
        x = F.leaky_relu(self.conv(x))
        x = self.flatten(x)
        x = self.linear(x)
        return x


