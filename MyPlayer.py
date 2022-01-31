"""
Alias for a player

"""

from playerInterface import *
from Board import *
from mcts_players import RolloutPlayer, NetworkPlayer


class myPlayer(PlayerInterface):
    """Alias to make my IDE at peace"""

    def __init__(self):
        self.board = None
        self.player = NetworkPlayer(turn_time=4)

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
        self.board = Board(x=True)
        self.player.new_game(color)

    def endGame(self, color):
        self.player.on_end(self.board, color - 1)
