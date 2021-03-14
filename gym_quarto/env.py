import gym
import logging
import numpy as np
import random

from .game import QuartoGame, QuartoPiece

logger = logging.getLogger(__name__)

class QuartoEnv(gym.Env):
    EMPTY = 0
    metadata = {'render.modes':['terminal']}

    def __init__(self):
        super(QuartoEnv, self).__init__()

        # action is [pos, next]
        # both are not null, they are just ignored when irrelevant
        self.action_space = gym.spaces.MultiDiscrete([16, 16])

        # next piece + board (flatten) 
        self.observation_space = gym.spaces.MultiDiscrete([17] * (1+4*4))

        self.reset()

    def reset(self, random_start=True):
        self.game = QuartoGame()
        self.turns = 0
        self.piece = None
        self.broken = False
        return self.observation

    def step(self, action):
        reward = 0
        info = {}
        if self.done:
            logger.warn("Actually already done")
            return self.observation, reward, self.done, info

        position, next = action
        logger.debug(f"Received: position: {position}, next: {next}")

        # Process the position
        if self.piece is not None:
            # Don't play on the first turn, just save the next piece
            valid = self.game.play(self.piece, (position % 4, position // 4))
            if not valid:
                # Invalid move
                reward = -200
                self.broken = True
            elif self.game.game_over:
                # We just won !
                reward = 100 + 16 - self.turns
            else:
                # We managed to play something valid
                reward = 5

        # Process the next piece
        self.piece = QuartoPiece(next)

        # Turn done
        self.turns += 1
        return self.observation, reward, self.done, info

    @property
    def observation(self):
        """ game board + next piece
        """
        board = []
        for row in self.game.board:
            for piece in row:
                if piece is None:
                    board.append(self.EMPTY)
                else:
                    board.append(QuartoEnv.pieceNum(piece) + 1)
        if self.piece is None:
            piece = [self.EMPTY]
        else :
            piece = [QuartoEnv.pieceNum(self.piece) + 1]
        return np.concatenate((piece, board)).astype(np.int8)

    @property
    def done(self):
        return self.broken or self.game.game_over

    def render(self, mode, **kwargs):
        for row in self.game.board:
            s = ""
            for piece in row:
                if piece is None:
                    s += ". "
                else:
                    s += str(piece) + " "
            print(s)
        print(f"Next: {self.piece}, Free: {''.join(str(p) for p in self.game.free)}")
        print()

    @classmethod
    def pieceNum(klass, piece):
        res = 0
        if piece.big:
            res += 1
        if piece.hole:
            res += 2
        if piece.black:
            res += 4
        if piece.round:
            res += 8
        return res

    def __del__(self):
        self.close()