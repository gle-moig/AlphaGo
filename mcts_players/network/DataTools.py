import os
import urllib.request as request
import gzip
import json
import numpy as np

from Constants import P
from Board import Board


def game_to_data(moves, v_b, v_w, k=7):
    board = Board(k=k, x=True)
    for i in range(len(moves)):
        yield board.x, [v_b, v_w][board.player], P[moves[i]]
        try:
            board.play(moves[i])
        except KeyError:
            break


def augment_data(_x, _v, _p):
    size = int((len(_p) - 1) ** 0.5)
    p_mat = np.reshape(_p[:-1], (size, size))
    for rot in range(4):
        x_rot = np.rot90(_x, rot, axes=(1, 2))
        p_rot = np.rot90(p_mat, rot, axes=(0, 1))
        for flip in [0, 1]:
            if flip:
                x_aug = np.flip(x_rot, axis=1)
                p_aug = np.flip(p_rot, axis=0)
            else:
                x_aug = x_rot
                p_aug = p_rot
            p_aug = np.concatenate([
                p_aug.flatten(),
                [_p[-1]]
            ])
            yield x_aug, _v, p_aug


def generate_data_files(data_dir):
    file = os.path.join(data_dir, "samples-9x9.json.gz")
    if not os.path.isfile(file):
        print("File", file, "not found, I am downloading it...", end="")
        request.urlretrieve("https://www.labri.fr/perso/lsimon/ia-inge2/samples-9x9.json.gz",
                            file)
        print(" Done")

    with gzip.open(file) as fd:
        data = json.loads(fd.read().decode("utf-8"))

    with open(os.path.join(data_dir, "x.data"), 'w') as f_x:
        with open(os.path.join(data_dir, "v.data"), 'w') as f_v:
            with open(os.path.join(data_dir, "p.data"), 'w') as f_p:
                i = 0
                for game_data in data:
                    try:
                        moves = list(map(Board.move_from_string, game_data["list_of_moves"]))
                    except ValueError:
                        # print(f"bad data line {i}")
                        i += 1
                        continue
                    v_b = game_data["black_wins"] / game_data["rollouts"]
                    v_w = game_data["white_wins"] / game_data["rollouts"]
                    for x, v, p in game_to_data(moves, v_b, v_w):
                        for _x, _v, _p in augment_data(x, v, p):
                            f_x.write(f"{json.dumps(_x.tolist())}\n")
                            f_v.write(f"{json.dumps(_v)}\n")
                            f_p.write(f"{json.dumps(_p.tolist())}\n")
                    i += 1
                    if i % 500 == 0:
                        print(f"parsed {i}/{len(data)} games")


if __name__ == '__main__':
    generate_data_files("./data")
