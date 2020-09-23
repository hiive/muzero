"""
File to perform small test runs on the codebase for both AlphaZero and MuZero.
"""

# Bugfxing TF2?
# Prevent TF2 from hogging all the available VRAM when initializing?
# @url: https://github.com/tensorflow/tensorflow/issues/24496#issuecomment-464909727
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
# Bugfxing TF2?

import json

import numpy as np

from utils.storage import DotDict
from AlphaZero.Coach import Coach
from hex.HexGame import HexGame as Game
from hex.AlphaZeroModel.NNet import NNetWrapper as HexNet
from hex.MuZeroModel.NNet import NNetWrapper as MuHexNet

ALPHAZERO_DEFAULTS = "Experimenter/Configs/SmallModel_AlphaZeroHex.json"
MUZERO_DEFAULTS = "Experimenter/MuZeroConfigs/default.json"

BOARD_SIZE = 5


def unpack_json(file: str):
    with open(file) as f:
        content = DotDict(json.load(f))
        name = content.name
        net_args = DotDict(content.net_args)
        args = DotDict(content.args)
    return name, net_args, args


def learnA0():
    name, net_args, args = unpack_json(ALPHAZERO_DEFAULTS)

    print("Testing:", name)

    g = Game(BOARD_SIZE)
    hex_net = HexNet(g, net_args)

    if args.load_model:
        hex_net.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, hex_net, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()

    c.learn()


def learnM0():
    name, net_args, args = unpack_json(MUZERO_DEFAULTS)

    print("Testing:", name)

    g = Game(BOARD_SIZE)
    hex_net = MuHexNet(g, net_args)

    if args.load_model:
        hex_net.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    b = g.getInitBoard()
    g.display(b)
    encoded = hex_net.encode(np.stack([b] * net_args.observation_length, axis=-1))
    print(encoded.shape)
    v, pi = hex_net.predict(encoded)

    r, latent_next = hex_net.forward(encoded, 2)
    print(r, latent_next.shape)


if __name__ == "__main__":
    # learnA0()
    learnM0()