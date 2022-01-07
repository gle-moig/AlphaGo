# import torch
# import torch.nn as nn
import numpy as np
import os
import urllib.request as request
import gzip
import json

from Board import *


def get_player_board(board, player):
    player_board = np.zeros_like(board)
    shape = board.shape
    for i in shape[0]:
        for j in shape[1]:
            if board[i][j] == player + 1:
                player_board[i][j] = 1
    return player_board

def preprocess(moves, size=9, k=7):
    player = 0  # black begins
    player_input = [
        np.zeros((size, size)),
        np.ones((size, size))
    ]
    model_inputs = np.zeros((size, size, 2*k + 1))
    board = Board()
    for move in moves:
        board.play(move)
        model_inputs = model_inputs[2:-1]
        model_inputs.extend([
            get_player_board(board, 0),
            get_player_board(board, 1)
        ])
        model_inputs.append(player_input[player])
        yield model_inputs
        player = 1 - player
        

if __name__== "__main__":
    file = "data/samples-9x9.json.gz"
    if not os.path.isfile(file):
        print("File", file, "not found, I am downloading it...", end="")
        request.urlretrieve("https://www.labri.fr/perso/lsimon/ia-inge2/samples-9x9.json.gz", "data/samples-9x9.json.gz")
        print(" Done")


    with gzip.open("data/samples-9x9.json.gz") as fd:
        data = json.loads(fd.read().decode("utf-8"))

    size = 9
    str_moves = [
        str_row + str_col
        for str_row in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        for str_col in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    ]
    k = 7
    batch_size = 32
    epochs = 10
    # todo: data in batch and training backprop
    for epoch in epochs:
        for game_data in data:
            moves = [
                str_moves.index(str_move) if str_move in str_moves else -1
                for str_move in game_data["list_of_moves"]
            ]
            vs = [game_data["black_wins"]/game_data["rollouts"],
                game_data["white_wins"]/game_data["rollouts"]]
            i = 0
            for training_data in preprocess(moves[:-1]):
                model(training_data)

            

    print(data)

