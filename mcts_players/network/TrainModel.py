import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, random_split, DataLoader
import os.path
import json

from mcts_players.network.Network import Network


class AlphaGoDataset(Dataset):
    def __init__(self, directory):
        self.f_x = open(f"{directory}/x.data", 'r')
        self.f_v = open(f"{directory}/v.data", 'r')
        self.f_p = open(f"{directory}/p.data", 'r')
        self.x_lines = self.f_x.readlines()
        self.v_lines = self.f_v.readlines()
        self.p_lines = self.f_p.readlines()
        l_x, l_v, l_p = len(self.x_lines), len(self.v_lines), len(self.p_lines)
        assert l_x == l_v == l_p
        self.length = l_x

    def close(self):
        self.f_x.close()
        self.f_v.close()
        self.f_p.close()

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        return np.array(json.loads(self.x_lines[idx])), \
               json.loads(self.v_lines[idx]), \
               np.array(json.loads(self.p_lines[idx]))


def train_model(data_dir, checkpoints_dir, save_dir, test_split, k, epochs):
    dataset = AlphaGoDataset(data_dir)
    train_split = int(len(dataset) * (1 - test_split))
    train_set, test_set = random_split(dataset, [train_split, len(dataset) - train_split])

    train_dataloader = DataLoader(train_set, batch_size=64, shuffle=True)
    test_dataloader = DataLoader(test_set, batch_size=64, shuffle=True)

    model = Network(k=k)
    v_loss_fn = nn.MSELoss()
    p_loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    softmax = nn.Softmax(dim=1)
    print("training...")
    for epoch in range(epochs):
        running_v_loss = 0.0
        running_p_loss = 0.0
        for i, (x, v, p) in enumerate(train_dataloader):
            x, v, p = x.float(), v.float(), p.float()
            optimizer.zero_grad()
            y_v, y_p = model(x)
            v_loss = v_loss_fn(y_v, v)
            v_loss.backward(retain_graph=True)
            p_loss = p_loss_fn(softmax(y_p), p)
            p_loss.backward()
            optimizer.step()
            running_v_loss += v_loss.item()
            running_p_loss += p_loss.item()
            if i % 2000 == 1999:
                print(
                    f"[{epoch + 1}, {i + 1:5d}/{len(train_dataloader)}]",
                    f"v_loss: {running_v_loss / 2000:.3f}",
                    f"p_loss: {running_p_loss / 2000:.3f}"
                )
                running_v_loss = 0.0
                running_p_loss = 0.0
                model.save(os.path.join(checkpoints_dir, f"checkpoint_{epoch + 1}_{i + 1}.pt"))
    model.save(save_dir)
    with torch.no_grad():
        v_loss = 0
        p_loss = 0
        i = 0
        for x, v, p in test_dataloader:
            x, v, p = x.float(), v.float(), p.float()
            y_v, y_p = model(x)
            v_loss = v_loss_fn(y_v, v).item()
            p_loss = p_loss_fn(y_p, p).item()
            i += 1
        print(f"on test set (size: {i}) v_loss: {v_loss / i} p_loss: {p_loss / i}")


if __name__ == "__main__":
    train_model(
        data_dir="./data",
        checkpoints_dir="./checkpoints",
        save_dir="./models/v0.pt",
        test_split=0.1,
        k=7,
        epochs=10
    )
