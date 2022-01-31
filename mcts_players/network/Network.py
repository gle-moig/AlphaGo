import torch
from torch import nn


class Network(nn.Module):
    def __init__(self, k=7, model_path=None):
        super(Network, self).__init__()
        # try layer norm
        self.conv_relu_stack = nn.Sequential(
            nn.Conv2d(in_channels=2*k + 1, out_channels=2*k + 1, kernel_size=(5, 5), padding="same"),
            nn.ReLU(),
            nn.BatchNorm2d(num_features=2*k + 1)
        )
        self.dense_relu_stack = nn.Sequential(
            nn.Flatten(),
            nn.Linear(9*9*(2*k + 1), 512),
            nn.ReLU(),
            nn.Linear(512, 128),
            nn.ReLU()
        )
        self.v_stack = nn.Sequential(
            nn.Linear(128, 1)
        )
        self.p_stack = nn.Sequential(
            nn.Linear(128, 82)
        )
        if model_path:
            self.load_state_dict(torch.load(model_path))

    def forward(self, x):
        x = torch.FloatTensor(x)
        for _ in range(5):
            x = self.conv_relu_stack(x) + x
        x = self.dense_relu_stack(x)
        v = self.v_stack(x).squeeze(dim=1)
        logits = self.p_stack(x)
        return v, logits

    def save(self, path):
        torch.save(self.state_dict(), path)
