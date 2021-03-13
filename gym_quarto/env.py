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
        self.action_space = gym.spaces.MultiDiscrete([17, 16])

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
        valid = True
        if self.turns != 0:
            # Don't play on the first turn
            valid = self.game.play(self.piece, (position % 4, position // 4))
        if not valid:
            reward = -200
            self.broken = True
        elif self.game.game_over:
            reward = 100 + 16 - self.turns
        self.piece = QuartoPiece(next)
        self.turns += 1
        return self.observation, reward, self.done, info

    @property
    def observation(self):
        """ game board + next piece
        """
        board = []
        for row in self.game.board:
            for piece in row:
                board.append(QuartoEnv.pieceNum(piece))
        piece = [QuartoEnv.pieceNum(self.piece)]
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
        if piece is None:
            return klass.EMPTY
        res = 0
        if piece.big:
            res += 1
        if piece.hole:
            res += 2
        if piece.black:
            res += 4
        if piece.round:
            res += 8
        return res+1 # empty = 0
