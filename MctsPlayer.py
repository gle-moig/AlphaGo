import Goban
from playerInterface import *

import numpy as np
import matplotlib.pyplot as plt
import go_plot
from MctsTree import MctsTree


class myPlayer(PlayerInterface):
    """ doc to do"""

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    def getPlayerName(self):
        return "Joueur MCTS LLM"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS"
        tree = MctsTree()
        # todo: loop based on time
        for _ in range(1):
            tree.grow(board=self._board)
        # compute probabilities
        probabilities = np.zeros(82)
        for some_move, value in tree.get_moves_value(2).items():
            probabilities[some_move] = value
        # Normalize them
        probabilities /= np.sum(probabilities)

        # We plot them
        go_plot.plot_play_probabilities(self._board, probabilities)
        plt.show()
        # choosing move randomly with probabilities weights
        move = np.random.choice(range(82), p=probabilities)
        # Correct number for PASS
        if move == 81:
            move = -1
        self._board.push(move)

        # New here: allows to consider internal representations of moves
        # print("I am playing ", self._board.move_to_str(move))
        # print("My current board :")
        # self._board.prettyPrint()

        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move)

    def playOpponentMove(self, move):
        # print("Opponent played ", move, "i.e. ", move) # New here
        #  the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move))

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")
