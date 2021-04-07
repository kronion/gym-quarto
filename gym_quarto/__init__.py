from .env import QuartoEnv, QuartoEnvV0
from .env1 import MoveEncoding, BoardEncoding
from .player import RandomPlayer, A2CPlayer, HumanPlayer, random_action
from .wrapper import OnePlayerWrapper

from gym.envs.registration import register

register(
    id='quarto-v0',
    entry_point='gym_quarto.env:QuartoEnvV0',
)

def make_v1():
    env = QuartoEnv()
    env = MoveEncoding(env)
    env = BoardEncoding(env)
    return env

register(
    id='quarto-v1',
    entry_point='gym_quarto:make_v1',
)
