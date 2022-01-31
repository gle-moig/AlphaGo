"""
Aliases to make my IDE at peace

"""
import Goban
import numpy as np

from Constants import MOVES


def get_player_board(board, player):
    player_board = np.zeros_like(board)
    shape = board.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if board[i][j] == player + 1:
                player_board[i][j] = 1
    return player_board


class Board:
    @staticmethod
    def move_from_string(s):
        return MOVES.index(s)

    def __init__(self, k=7, x=False):
        self.k = k
        self.history = []
        self.moves = []
        self._board = Goban.Board()
        self._x = x
        if x:
            size, _ = self.shape
            self.x = np.zeros((2 * k + 1, size, size))
            self.player_input = [
                np.zeros((size, size)),
                np.ones((size, size))
            ]
            self.player = 0

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
        self.moves.append(move)
        is_legal = self._board.push(-1 if move == 81 else move)
        self.history.append(self.board)
        if self._x:
            self.x = np.concatenate([
                self.x[2:-1],
                [get_player_board(self.board, 0)],
                [get_player_board(self.board, 1)],
                [self.player_input[self.player]]
            ], 0)
            self.player = 1 - self.player
        return is_legal

    def undo(self):
        self._board.pop()
        self.history.pop()
        self.moves.pop()
        if self._x:
            self.player = 1 - self.player
            if len(self.history) < self.k:
                self.x = np.concatenate([
                    np.zeros_like(self.x[:2]),
                    self.x[:-3],
                    [self.player_input[self.player]]
                ], 0)
            else:
                self.x = np.concatenate([
                    [get_player_board(self.history[-self.k], 0)],
                    [get_player_board(self.history[-self.k], 1)],
                    self.x[:-3],
                    [self.player_input[self.player]]
                ], 0)
