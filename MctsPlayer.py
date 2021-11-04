from MctsTree import MctsTree


def get_move(game):
    tree = MctsTree()
    # todo: loop based on time
    for _ in range(5):
        tree.grow(game.copy())
    return tree.get_move(2)
