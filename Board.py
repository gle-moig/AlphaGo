"""
Aliases to allow me to code properly

"""
import Goban

class Board:
    def __init__(self):
        self._board = Goban.Board()
        self.history = []

    @property
    def board(self):
        return np.reshape(self._board[:], self.shape)

    @property
    def is_over(self):
        return self._board.is_game_over()

    @property
    def shape(self):
        size = int(len(self._board) ** .5)
        return size, size

    def get_moves(self, weak=False):
        if weak:
            moves = self._board.weak_legal_moves()
        else:
            moves = self._board.legal_moves()
        moves.remove(-1)
        moves.append(len(self._board))
        return moves

    def play(self, move):
        if move == 81:
            move = -1
        is_legal = self._board.push(move)
        self.history.append(self.board)
        return is_legal

    def undo(self):
        self._board.pop()
        self.history.pop()
