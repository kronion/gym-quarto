import gym
import numpy as np
import random

from .game import QuartoGame, QuartoPiece

class QuartoEnv(gym.Env):
    metadata = {'render.modes':['terminal']}

    def __init__(self):
        super(QuartoEnv, self).__init__()

        # action is [pos, next]
        self.action_space = gym.spaces.Box(
                low =0, high=16, shape=(2,), dtype=np.uint8)


        self.reset()

    def reset(self, random_start=True):
        self.game = QuartoGame()
        self.turns = 0
        self.piece = None

    def step(self, action):
        reward = 0
        info = {}
        if self.done:
            logger.warn("step() shouldn't have been called")
        else:
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

    @property
    def done(self):
        return self.game.game_over

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

    def step(self, action):
        obs, rew, done, info = super(OnePlayerQuartoEnv, self).step(action)
        if not done:
            # Let other play
            action = self.other_player.step()
            obs, _, done, _ = super(OnePlayerQuartoEnv, self).step(action)
        return obs, rew, done, info