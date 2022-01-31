import sys
import time
from random import shuffle
import numpy as np

from RolloutTree import RolloutTree


class RolloutPlayer:
    """ doc to do"""

    @staticmethod
    def rollout(board):
        i = 0
        while not board.is_over:
            moves = board.get_moves(weak=True)
            shuffle(moves)
            for move in moves:
                if board.play(move):
                    break
                board.undo()
            i += 1
        for _ in range(i):
            board.undo()
        return (i + 1) % 2

    def __init__(self, turn_time=20):
        self._color = None
        self.turn_time = turn_time

    @property
    def color(self):
        return self._color

    @property
    def name(self):
        return "Joueur MCTS avec rollouts"

    def new_game(self, color):
        self._color = color

    def get_next_move(self, board):
        if board.is_over:
            return 81  # pass move
        tree = RolloutTree()
        t = time.time()
        i = 0
        while time.time() - t < self.turn_time:
            tree.grow(board=board, rollout=self.rollout)
            i += 1
        print(f"Tree grown {i} times", file=sys.stderr)
        s, _ = board.shape
        # compute probabilities
        p = tree.get_p(size=1 + s ** 2, tau=2)
        # choosing move randomly with probabilities weights
        move = np.random.choice(range(82), p=p)
        return move

    def on_end(self, board, winner):
        pass
