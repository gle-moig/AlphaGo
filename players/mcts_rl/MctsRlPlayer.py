import numpy as np
from MctsRlTree import MctsRlTree
from MctsRlNn import MctsRlNn


class MctsRlPlayer:
    """ doc to do"""
    def __init__(self, color):
        self._color = color
        self.model = MctsRlNn(k=7, model_path="models/alpha_go.pt").to("cuda")
        self.targets_p = []

    @property
    def color(self):
        return self._color

    @property
    def name(self):
        return "Joueur MCTS avec apprentissage"

    def get_next_move(self, board):
        if board.is_over:
            return 81  # pass move
        tree = MctsRlTree()
        # todo: loop based on time
        for _ in range(2):
            tree.grow(board=board, model=self.model)
        s, _ = board.shape
        # compute probabilities
        self.targets_p.append(tree.get_p(size=1 + s ** 2, tau=2))
        # choosing move randomly with probabilities weights
        move = np.random.choice(range(82), p=self.targets_p[-1])
        return move

    def on_end(self, is_winner):
        if is_winner:
            print("I won!!!")
        else:
            print("I lost :(!!")
        # todo do backprop
