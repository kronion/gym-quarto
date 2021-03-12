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

class OnePlayerQuartoEnv(QuartoEnv):
    """ We emulate the second player so that each step is seen from the same player
    """
    def __init__(self, other_player):
        super(OnePlayerQuartoEnv, self).__init__(self)
        self.other_player = other_player

    def reset(self):
        super(OnePlayerQuartoEnv, self).reset()
        self.other_player.reset(self.game)
        self.other_first = random.choice([True, False])
        if self.other_first:
            # Make the first step now
            action = self.other_player.step()
            obs, _, done, _ = super(OnePlayerQuartoEnv, self).step(action)

        return self.observation

    def step(self, action):
        obs, rew, done, info = super(OnePlayerQuartoEnv, self).step(action)
        if not done:
            # Let other play
            action = self.other_player.step()
            obs, _, done, _ = super(OnePlayerQuartoEnv, self).step(action)
        return obs, rew, done, info