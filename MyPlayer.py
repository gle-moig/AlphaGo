"""
Aliases to allow me to code properly

"""
import numpy as np

from playerInterface import *
from players import *
from Board import *

PLAYER = MctsRlPlayer

class myPlayer(PlayerInterface):
    """Alias to fulfill bad code restrictions"""

    def __init__(self):
        self.player = object.__new__(PLAYER)
        self.board = Board()

    def getPlayerName(self):
        return self.player.name

    def getPlayerMove(self):
        move = self.player.get_next_move(self.board)
        self.board.play(move)
        if move == 81:
            move = -1
        return Goban.Board.flat_to_name(move)

    def playOpponentMove(self, move):
        move = Goban.Board.name_to_flat(move)
        if move == -1:
            move = 81
        self.board.play(move)

    def newGame(self, color):
        self.player.__init__(color)

    def endGame(self, color):
        self.player.on_end(color == self.player.color)
