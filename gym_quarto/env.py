import gym
import numpy as np
import random

from .game import QuartoGame, QuartoPiece

class QuartoEnv(gym.Env):
    EMPTY = -1
    metadata = {'render.modes':['terminal']}

    def __init__(self):
        super(QuartoEnv, self).__init__()

        # action is [pos, next]
        self.action_space = gym.spaces.Box(
                low =self.EMPTY, high=15, shape=(2,), dtype=np.int8)

        self.observation_space = gym.spaces.Box(
            low = self.EMPTY, high=15, shape=(17,), dtype=np.int8)

        self.reset()

    def reset(self, random_start=True):
        self.game = QuartoGame()
        self.turns = 0
        self.piece = None
        return self.observation

    def step(self, action):
        reward = 0
        info = {}
        assert not self.done
        
        position, next = action
        valid = self.game.play(self.piece, (position % 4, position // 4))
        if valid:
            pass                                  
        self.piece = QuartoPiece(next)

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
        return self.game.game_over

    def render(self, mode, **kwargs):
        pass

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
        return res
