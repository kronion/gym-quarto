import logging
import random

from stable_baselines3 import A2C

from .env import QuartoEnv
from .game import QuartoPiece

logger = logging.getLogger(__name__)

class RandomPlayer:
    def __init__(self, env):
        assert isinstance(env.unwrapped, QuartoEnv), env
        self.env = env

    def reset(self, env):
        pass

    def predict(self, obs):
        possible_actions = [a for a in self.env.legal_actions]
        return random.choice(possible_actions), None

    def seed(self, seed):
        random.seed(seed)

def random_action(game, buf_next):
    """ Random free piece, random free spot
    """
    if buf_next != 0:
        buf_next = QuartoPiece(buf_next - 1)
    if len(game.free) > 1:
        while True:
            next = random.choice(game.free)
            if next != buf_next:
                break
        next_p = QuartoEnv.pieceNum(next)
    else:
        next = None
        next_p = None
    
    while True:
        x = random.randrange(4)
        y = random.randrange(4)
        if game.board[y][x] is None:
            break

    logger.info(f"Playing random at ({x}, {y}), next: {next}")
    return x + y * 4, next_p

class A2CPlayer:
    def __init__(self, model_path, env):
        self.model = A2C.load(model_path, env)

    def reset(self, game):
        pass

    def predict(self, obs):
        return self.model.predict(obs)

    def seed(self, seed):
        pass

class HumanPlayer:
    def reset(self, game):
        print("Reseting game")

    def predict(self, obs):
        print("Your turn:")
        position = input("Where do you play? ")
        position = int(position[0]) + int(position[1]) * 4
        next_piece = input("Your next piece? ")
        next_piece = QuartoEnv.pieceFromStr(next_piece)
        return (position, next_piece), None

    def seed(self, seed):
        pass

