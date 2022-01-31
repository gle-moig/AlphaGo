import sys
import time
import numpy as np
import torch
from torch import nn

from Network import Network
from NetworkTree import NetworkTree
from DataTools import augment_data, game_to_data


class NetworkPlayer:
    """ doc to do"""
    def __init__(self, turn_time=20):
        self._color = None
        self.turn_time = turn_time
        self.model = Network(k=7, model_path="mcts_players/network/checkpoints/checkpoint_1_2000.pt")
        self.targets_p = []
        self.v_loss_fn = nn.MSELoss()
        self.p_loss_fn = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-3)
        self.softmax = nn.Softmax(dim=1)

    @property
    def color(self):
        return self._color

    @property
    def name(self):
        return "Joueur MCTS avec apprentissage"

    def new_game(self, color):
        self._color = color

    def get_next_move(self, board):
        if board.is_over:
            return 81  # pass move
        tree = NetworkTree()
        t = time.time()
        i = 0
        while time.time() - t < self.turn_time:
            tree.grow(board=board, model=self.model)
            i += 1
        print(f"Tree grown {i} times", file=sys.stderr)
        s, _ = board.shape
        # compute probabilities
        self.targets_p.append(tree.get_p(size=1 + s ** 2, tau=2))
        # choosing move randomly with probabilities weights
        move = np.random.choice(range(82), p=self.targets_p[-1])
        return move

    def on_end(self, board, winner):
        for x, v, p in game_to_data(board.moves, 1 - winner, winner, k=board.k):
            for _x, _v, _p in augment_data(x, v, p):
                y_v, y_p = self.model(_x)
                v_loss = self.v_loss_fn(y_v, v)
                v_loss.backward(retain_graph=True)
                p_loss = self.p_loss_fn(self.softmax(y_p), p)
                p_loss.backward()
                self.optimizer.step()

