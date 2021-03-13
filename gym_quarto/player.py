import logging
import random

from .env import QuartoEnv
from .game import QuartoPiece

logger = logging.getLogger(__name__)

class RandomPlayer:
    def reset(self, game):
        self.game = game

    def step(self, obs):
        return random_action(self.game, obs[0])

def random_action(game, buf_next):
    """ Random free piece, random free spot
    """
    if buf_next != 0:
        buf_next = QuartoPiece(buf_next)
    if len(game.free) > 1:
        while True:
            next = random.choice(game.free)
            if next != buf_next:
                break
    else:
        next = None
    while True:
        x = random.randrange(4)
        y = random.randrange(4)
        if game.board[y][x] is None:
            break

    logger.info(f"Playing random at ({x}, {y}), next: {next}")
    return x + y * 4, QuartoEnv.pieceNum(next)
