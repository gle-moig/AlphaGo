from numpy.random import choice

C_PUCT = 1


def rollout(game, depth=-1):
    player = game.player
    while not (game.is_over or depth == 0):
        game.play(choice(game.legal_moves))
        if depth > 0:
            depth -= 1
    while not game.is_over:
        game.play(-1)
    result = int(game.get_score() < 0)
    return 1 if result == player else 0


class Node:
    def __init__(self, move, parent=None):
        self.move = move
        self.children = []
        self.parent = parent
        self.p = 1
        self.n = 0
        self.w = 0

    @property
    def q(self):
        """
        Mean action value
        """
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
        return max(self.children, key=lambda child: child.q + child.u)


class MctsTree:
    def __init__(self):
        self.root = Node(None)

    def grow(self, game):
        """
        Does a step of MCTS

        Select best leaf then create its children based on possibles moves.
        For each child created, does a rollout and update every ancestors with the outcome

        :param game:
        :return:
        """
        current_node = self.root
        while len(current_node.children) > 0:
            current_node = current_node.favorite_child
            game.play(current_node.move)
        # remove dumb moves
        moves = []
        for move in game.legal_moves:
            if move != -1 and \
                all([game.state.board[j] == game.player and
                    game.state.chain_liberties(j, game.player, break_value=2) >= 2
                    for j in game.state.get_neighbors(move)]):
                continue
            moves.append(move)
        for move in moves:
            current_node.children.append(Node(move=move, parent=current_node))
        for child in current_node.children:
            child_game = game.copy()
            child_game.play(child.move)
            w = rollout(child_game, depth=10)
            current_ancestor = child
            current_ancestor.w += w
            current_ancestor.n += 1
            while current_ancestor.parent is not None:
                current_ancestor = current_ancestor.parent
                current_ancestor.w += w
                current_ancestor.n += 1

    def get_moves_value(self, tau):
        """
        compute each move value with the current tree knowledge

        :param tau: temperature
        :return moves_value: dict with move:value
        """
        if tau == 0:
            return {self.root.favorite_child.move: 1}
        denominator = sum([child.n ** (1 / tau) for child in self.root.children])
        return {child.move: child.n ** (1 / tau) / denominator for child in self.root.children}

    def get_move(self, tau):
        moves, probabilities = zip(*self.get_moves_value(tau).items())
        return choice(moves, p=probabilities)
