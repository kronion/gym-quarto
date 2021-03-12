import random

from .env import QuartoEnv

class RandomPlayer:
    def reset(self, game):
        self.game = game

    def step(self):
        return random_action(self.game)

def random_action(game):
    """ Random free piece, random free spot
    """
    if game.free:
        next = QuartoEnv.pieceNum(random.choice(game.free))
    else:
        next = QuartoEnv.EMPTY
    while True:
        x = random.randrange(4)
        y = random.randrange(4)
        if game.board[y][x] is None:
            return x + y * 4, next
