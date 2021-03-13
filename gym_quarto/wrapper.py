import random

from gym import Wrapper

class OnePlayerWrapper(Wrapper):
    """ We emulate the second player so that each step is seen from the same player
    """
    def __init__(self, env, other_player):
        super(OnePlayerWrapper, self).__init__(env)
        self.other_player = other_player

    def reset(self):
        super(OnePlayerWrapper, self).reset()
        self.other_player.reset(self.game)
        self.other_first = random.choice([True, False])
        if self.other_first:
            # Make the first step now
            action = self.other_player.step()
            obs, _, done, _ = self.env.step(action)

        return self.observation

    def step(self, action):
        obs, rew, done, info = self.env.step(action)
        if not done:
            # Let other play
            action = self.other_player.step()
            obs, _, done, _ = self.env.step(action)
        return obs, rew, done, info