import sys

from mcts_players.MctsTree import MctsTree, Node


class NetworkTree(MctsTree):
    def __init__(self):
        super().__init__()

    def grow(self, board, model):
        """
        Does a step of MCTS

        Select best leaf then create its children based on possibles moves.
        For each child created, does a rollouts and update every ancestors with the outcome

        :param board:
        :param model:
        :return:
        """
        current_node = self.root
        while len(current_node.children) > 0:
            current_node = current_node.favorite_child
            board.play(current_node.move)
        can_play = not board.is_over
        if can_play:
            [v], [p] = model([board.x])
            moves = board.get_moves()
            for move in moves:
                current_node.children.append(Node(move=move, parent=current_node, p=p[move]))
            current_node.w += v
            current_node.n += 1
        while current_node.parent is not None:
            current_node = current_node.parent
            if can_play:
                current_node.w += v
                current_node.n += 1
            # reset the board
            board.undo()
