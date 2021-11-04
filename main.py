#!python3.8

import sys
import importlib
import time

import GoFast


def main(*argv):
    argv_are_valid = len(argv) == 3 and\
        len(argv[1]) > 3 and argv[1][-3:] == ".py" and\
        len(argv[2]) > 3 and argv[2][-3:] == ".py"
    if not argv_are_valid:
        print("""
Error: wrong arguments

Please launch game with command:
```python main.py black_player.py white_player.py```
    
""", file=sys.stderr)
        return 1
    get_black_move = getattr(importlib.import_module(argv[1][:-3]), "get_move")
    get_white_move = getattr(importlib.import_module(argv[2][:-3]), "get_move")
    game = GoFast.Game(9)
    print(game)
    while not game.is_over:
        t0 = time.time()
        if game.player_color == "black":
            move = get_black_move(game.copy())
        elif game.player_color == "white":
            move = get_white_move(game.copy())
        else:
            raise Exception("Unknown Color")
        t1 = time.time()
        game.play(move)
        t2 = time.time()
        print(game)
        print(f"processing time: {t1 - t0}; play time: {t2 - t1}")


if __name__ == '__main__':
    main(*sys.argv)
