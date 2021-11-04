from copy import deepcopy
from enum import Enum
import numpy as np


class Player(Enum):
    NONE = 0
    BLACK = 1
    WHITE = 2

    def __invert__(self):
        if self.value == Player.WHITE:
            return Player.BLACK
        if self.value == Player.BLACK:
            return Player.WHITE
        return Player.NONE


class _State:
    def __init__(self, size):
        """
        :param size: size of the board
        """
        self._size = size
        self._board = np.array([Player.NONE] * size ** 2, dtype=Player)
        self._captures = {Player.BLACK: 0, Player.WHITE: 0}

    @property
    def size(self):
        """
        :return size: size of the board
        """
        return self._size

    @property
    def board(self):
        """
        :return board: goban at current state of the game. cells are 0 for empty cells, 1 for blacks, 2 for whites
        """
        return tuple(self._board)

    @property
    def captures(self):
        """
        :return captures: list of number of stones captured by each player
                          (index 0: black player; index 1: white player)
        """
        return _FrozenDict(self._captures)

    def tbr_update(self):
        return self._update

    def tbr_get_score(self):
        return self._get_score

    def get_legal_moves(self, player, last_two_moves):
        if last_two_moves == [-1, -1]:
            return []
        moves = [-1]
        for i in range(len(self._board)):
            if self.board[i] == 0:
                # free
                if self.chain_liberties(i, player, break_value=1) >= 1:
                    moves.append(i)
                    continue
                # ko
                if i == last_two_moves[0]:
                    continue
                # create its liberty
                for j in self.get_neighbors(i):
                    if self.board[j] == 3 - player and \
                            not (self.chain_liberties(j, 3 - player, break_value=2) >= 2):
                        moves.append(i)
                        break
        return moves

    def get_neighbors(self, i):
        assert 0 <= i < self.size ** 2
        if i == 0:
            return [i + 1, i + self.size]
        if i == self.size - 1:
            return [i - 1, i + self.size]
        if i == self.size * (self.size - 1):
            return [i - self.size, i + 1]
        if i == self.size ** 2 - 1:
            return [i - 1, i - self.size]
        if i % self.size == 0:
            return [i - self.size, i + 1, i + self.size]
        if i // self.size == 0:
            return [i - 1, i + 1, i + self.size]
        if i % self.size == self.size - 1:
            return [i - 1, i - self.size, i + self.size]
        if i // self.size == self.size - 1:
            return [i - 1, i - self.size, i + 1]
        return [i - 1, i - self.size, i + 1, i + self.size]

    def chain_liberties(self, i, player, break_value=None):
        liberties = 0
        border = [i]
        history = []
        while len(border) > 0:
            current = border.pop()
            for neighbor in self.get_neighbors(current):
                if neighbor not in history:
                    if self.board[neighbor] == 0:
                        liberties += 1
                        if break_value is not None and liberties >= break_value:
                            return liberties
                        continue
                    if self.board[neighbor] == player:
                        border.append(neighbor)
                        history.append(current)
        return liberties

    def get_territory(self, i, break_if_unowned=False):
        assert self.board[i] == 0
        border = [i]
        history = []
        player = 0
        while len(border) > 0:
            current = border.pop()
            for neighbor in self.get_neighbors(current):
                value = self.board[neighbor]
                if neighbor not in history:
                    if player != 3 and value == 3 - player:
                        if break_if_unowned:
                            return history, 0
                        player = 3
                    if player == 0 and value != 0:
                        player = value
                    if value == 0:
                        border.append(neighbor)
            history.append(current)
        return history, player % 3

    def _update(self, move, player):
        self._board[move] = player
        for j in self.get_neighbors(move):
            if self.board[j] == 3 - player and not (self.chain_liberties(j, 3 - player, break_value=1) >= 1):
                self._capture(j)

    def _capture(self, i):
        assert self.board[i] != 0
        player = self.board[i]
        self._board[i] = 0
        self._captures[2 - player] += 1
        border = [i]
        while len(border) > 0:
            current = border.pop()
            for neighbor in self.get_neighbors(current):
                if self.board[neighbor] == player:
                    self._board[neighbor] = 0
                    self._captures[2 - player] += 1
                    border.append(neighbor)

    def _get_score(self):
        """
        Computes black score. Negative if white are the winner.

        Komi is worth -7.5
        """
        # remove dead stones
        # todo: effective dead stone removal
        for i in range(len(self.board)):
            if self.board[i] != 0:
                if not (self.chain_liberties(i, self.board[i], break_value=2) >= 2):
                    self._capture(i)
        history = []
        score = -7.5 + self.board.count(0) - self.board.count(1)
        for i in range(len(self.board)):
            if i not in history and self.board[i] == 0:
                territory, player = self.get_territory(i)
                if player == 1:
                    score += len(territory)
                elif player == 2:
                    score -= len(territory)
                history.extend(territory)
        return score


class Game:
    def __init__(self, size=19):
        self._state = _State(size)
        self._state_update = self._state.tbr_update()
        self._state_get_score = self._state.tbr_get_score()
        delattr(self._state.__class__, "tbr_update")
        delattr(self._state.__class__, "tbr_get_score")
        self._player = 1
        self._history = []
        self._legal_moves = self._state.get_legal_moves(self._player, [None, None])

    @property
    def state(self):
        return self._state

    @property
    def player(self):
        return self._player

    @property
    def player_color(self):
        return ["black", "white"][self._player - 1]

    @property
    def history(self):
        return _FrozenList(self._history)

    @property
    def legal_moves(self):
        return _FrozenList(self._legal_moves)

    @property
    def is_over(self):
        return self.legal_moves == []

    def play(self, move):
        assert move in self.legal_moves
        if move != -1:
            self._state_update(move=move, player=self.player)
        self._history.append(move)
        self._player = 3 - self._player
        last_two_moves = [None, None] if len(self.history) < 2 else self.history[-2:]
        self._legal_moves = self.state.get_legal_moves(self.player, last_two_moves)

    def get_score(self):
        assert self.is_over
        return self._state_get_score()

    def __repr__(self):
        board = []
        for i in range(len(self.state.board)):
            stone_key = self.state.board[i]
            stone = ['+', "\033[30m●", "\033[37m●"][stone_key]
            if stone_key == 0 and i not in self.legal_moves:
                stone = "\033[30m" + stone
            elif stone_key != 0 and len(self.history) > 0 and i == self.history[-1]:
                stone = stone[:-1] + '◉'
            board.append(stone + "\033[0m")
        footer = []
        if len(self.history) > 0:
            if self.history[-1] == -1:
                footer.append("Player passed.")
            footer.append("Black captured {} and white {}.".format(*self.state.captures))
        if not self.is_over:
            footer.append("{}'s turn.".format(self.player_color.capitalize()))
        else:
            score = self.get_score()
            if score > 0:
                winner = "black"
            else:
                winner = "white"
            footer.append("{} won by {} points.".format(winner.capitalize(), abs(score)))
        return "\n".join([" ".join(board[i:i + self.state.size])
                          for i in range(0, self.state.size ** 2, self.state.size)] + footer)

    def copy(self):
        return deepcopy(self)


if __name__ == "__main__":
    game = Game(size=9)
    game.play(11)
    game.play(12)
    game2 = game.copy()
    game.play(19)
    game.play(22)
    game.play(29)
    game.play(30)
    game.play(21)
    print(game, end="\n\n")
    game.play(20)
    print(game, end="\n\n")
    print(21 in game.legal_moves)
    print(game2, end="\n\n")
    try:
        game.play(21)
    except AssertionError:
        print("KO rule working")
    else:
        print("KO not working")
