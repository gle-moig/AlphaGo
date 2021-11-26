from random import choice

C_PUCT = 1


class Node:
    def __init__(self, move=None, parent=None):
        self.move = move
        self.children = []
        self.parent = parent
        self.p = 1
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

    def grow(self, board):
        """
        Does a step of MCTS

        Select best leaf then create its children based on possibles moves.
        For each child created, does a rollout and update every ancestors with the outcome

        :param board:
        :return:
        """
        current_node = self.root
        while len(current_node.children) > 0:
            current_node = current_node.favorite_child
            board.push(current_node.move)
        # recup p et v du reseau

        # for move in board.legal_moves():
        #     current_node.children.append(Node(move=move, parent=current_node))
        # for child in current_node.children:
        #     board.push(child.move)
        #     w = rollout(board)
        #     current_ancestor = child
        #     current_ancestor.w += w
        #     current_ancestor.n += 1
        #     while current_ancestor.parent is not None:
        #         current_ancestor = current_ancestor.parent
        #         current_ancestor.w += w
        #         current_ancestor.n += 1
        #     board.pop()
        # reset the board
        while current_node.parent is not None:
            current_node = current_node.parent
            board.pop()

    def get_moves_value(self, tau):
        """
        compute each move value with the current tree knowledge

        :param tau: temperature
        :return moves_value: dict with move:value
        """
        denominator = sum([child.n ** (1 / tau) for child in self.root.children])
        return {child.move: child.n ** (1 / tau) / denominator for child in self.root.children}
