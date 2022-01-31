import numpy as np

from Constants import C_PUCT


class Node:
    def __init__(self, move=None, parent=None, p=1):
        self.move = move
        self.children = []
        self.parent = parent
        self.p = p
        self.n = 0
        self.w = 0

    @property
    def q(self):
        assert self.w <= self.n
        if self.n == 0:
            return 1
        return self.w / self.n

    @property
    def u(self):
        assert self.parent is not None
        return C_PUCT * self.p * self.parent.n ** 0.5 / (1 + self.n)

    @property
    def favorite_child(self):
        assert len(self.children) > 0
        return max(self.children, key=lambda _child: _child.q + _child.u)


class MctsTree:
    def __init__(self):
        self.root = Node()

    def grow(self, board, func):
        """
        Does a step of MCTS

        Select best leaf then create its children based on possibles moves.
        For each child created, evaluate it and update every ancestors with the outcome

        :param board:
        :param func:
        :return:
        """
        raise NotImplementedError

    def get_p(self, size, tau):
        """
        compute each move value with the current tree knowledge

        :param size: number of moves possible
        :param tau: temperature
        :return moves_value: dict with move:value
        """
        p = np.zeros(size)
        if tau == 0:
            tau = 1e-7
        denominator = sum([child.n ** (1 / tau) for child in self.root.children])
        for child in self.root.children:
            p[child.move] = child.n ** (1 / tau) / denominator
        return p
