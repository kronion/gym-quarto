from gym.envs.registration import register

from .env import QuartoEnv
from .env1 import MoveEncoding
from .player import RandomPlayer, A2CPlayer, HumanPlayer, random_action
from .wrappers.actions import TwoChoiceEncoding
from .wrappers.observations import ObsBoxEncoding, ObsMultiDiscreteEncoding


register(
    id='quarto-v0',
    entry_point='gym_quarto.env:QuartoEnvV0',
)


def make_v1():
    env = QuartoEnv()
    env = MoveEncoding(env)
    env = ObsBoxEncoding(env)
    return env


def make_multidiscrete():
    env = QuartoEnv()
    env = TwoChoiceEncoding(env)
    env = ObsMultiDiscreteEncoding(env)
    return env


register(
    id='quarto-v1',
    entry_point='gym_quarto:make_v1',
)


register(
    id="quarto-multidiscrete-v1",
    entry_point="gym_quarto:make_multidiscrete",
)
