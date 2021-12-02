from random import choice, shuffle
import numpy as np

from MctsTree import MctsTree


class MctsRolloutPlayer:
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

    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

    @property
    def name(self):
        return "Joueur MCTS avec rollouts"

    def get_next_move(self, board):
        if board.is_over:
            return 81  # pass move
        tree = MctsTree()
        # todo: loop based on time
        for _ in range(2):
            tree.grow(board=board, rollout=self.rollout)
        s, _ = board.shape
        # compute probabilities
        p = tree.get_p(size=1 + s ** 2, tau=2)
        # choosing move randomly with probabilities weights
        move = np.random.choice(range(82), p=p)
        return move

    def on_end(self, is_winner):
        if is_winner:
            print("I won!!!")
        else:
            print("I lost :(!!")
