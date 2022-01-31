from mcts_players.MctsTree import MctsTree, Node


class RolloutTree(MctsTree):
    def __init__(self):
        super().__init__()

    def grow(self, board, rollout):
        """
        Does a step of MCTS

        Select best leaf then create its children based on possibles moves.
        For each child created, does a rollouts and update every ancestors with the outcome

        :param board:
        :param rollout:
        :return:
        """
        current_node = self.root
        while len(current_node.children) > 0:
            current_node = current_node.favorite_child
            board.play(current_node.move)
        if not board.is_over:
            moves = board.get_moves()
            for move in moves:
                current_node.children.append(Node(move=move, parent=current_node))
            for child in current_node.children:
                board.play(child.move)
                w = rollout(board)
                current_ancestor = child
                current_ancestor.w += w
                current_ancestor.n += 1
                while current_ancestor.parent is not None:
                    current_ancestor = current_ancestor.parent
                    current_ancestor.w += w
                    current_ancestor.n += 1
                board.undo()
        # reset the board
        while current_node.parent is not None:
            current_node = current_node.parent
            board.undo()
