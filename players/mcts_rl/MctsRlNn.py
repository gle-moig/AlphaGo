import torch
from torch import nn


class MctsRlNn(nn.Module):
    @staticmethod
    def format_input(board):
        pass

    def __init__(self, k=7, model_path=None):
        super(MctsRlNn, self).__init__()
        if model_path:
            self.load_state_dict(torch.load(model_path))
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

    def forward(self, x):
        for _ in range(5):
            x = self.conv_relu_stack(x) + x
        x = self.dense_relu_stack(x)
        v = self.v_stack(x)
        logits = self.p_stack(x)
        return v, logits

    def save(self, path):
        torch.save(self.state_dict(), path)


if __name__ == "__main__":
    model = MctsRlNn().to("cuda")
    value_loss_fn = nn.MSELoss()
    p_loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    data = ...
    for x, target_value, target_p in data:
        x, target_value, target_p = x.to("cuda"), target_value.to("cuda"), target_p.to("cuda")
        pred_value, pred_logits = model(x)
        value_loss = value_loss_fn(pred_value, target_value)
        value_loss.backward()
        p_loss = p_loss_fn(nn.Softmax(pred_logits), target_p)
        p_loss.backward()
        optimizer.zero_grad()
        optimizer.step()

    print(model)
