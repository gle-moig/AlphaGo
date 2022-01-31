# Alphago

## run

- with poetry
```shell
pip install poetry
poetry install
poetry run python namedGame.py randomPlayer.py MyPlayer.py
```

- without
```shell
pip install numpy
pip install torch
pip install matplotlib
python namedGame.py randomPlayer.py MyPlayer.py
```

## change player or turn time

see `MyPlayer.py` line 16

## change model

see `mcts_players/network/NetworkPlayer.py` line 17

## train model

create `mcts_players/network/checkpoints` and `mcts_players/network/models` directories.

run files `mcts_players/network/DataTools.py` and `mcts_players/network/TrainModel.py`
