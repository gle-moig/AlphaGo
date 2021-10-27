import Goban
from playerInterface import *

import numpy as np
import matplotlib.pyplot as plt
from random import sample
import go_plot


def rollout(board, player=1):
    if board.is_game_over():
        return player
    move = sample(board.legal_moves(), 1)[0]
    board.push(move)
    res = rollout(board, not player)
    board.pop()
    return res


def get_value(board, move):
    nb_sim = 5
    board.push(move)
    total = 0
    for i in range(nb_sim):
        total += rollout(board)
    board.pop()
    return total/nb_sim


class myPlayer(PlayerInterface):
    """ Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    """

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    def getPlayerName(self):
        return "MCS Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS"
        # Get the list of all possible moves
        moves = self._board.legal_moves()  # Dont use weak_legal_moves() here!
        # Generate eval by rolling out
        eval_moves = {}
        for some_move in moves:
            eval_moves[some_move] = get_value(self._board, some_move)
        # compute probabilities
        probabilities = np.zeros(82)
        for some_move, value in eval_moves.items():
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
        #print("I am playing ", self._board.move_to_str(move))
        #print("My current board :")
        #self._board.prettyPrint()

        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move)

    def playOpponentMove(self, move):
        #print("Opponent played ", move, "i.e. ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move))

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")
