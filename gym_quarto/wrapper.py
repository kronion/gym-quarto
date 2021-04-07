import random

from gym import Wrapper
from gym.envs.registration import register

class OnePlayerWrapper(Wrapper):
    """ We emulate the second player so that each step is seen from the same player
    """
    def __init__(self, env, other_player):
        super(OnePlayerWrapper, self).__init__(env)
        self.other_player = other_player

    def reset(self):
        obs = self.env.reset()
        self.other_player.reset(self.game)
        self.other_first = random.choice([True, False])
        if self.other_first:
            # Make the first step now
            action, _ = self.other_player.predict(obs)
            obs, _, done, _ = self.env.step(action)

        return obs

    def step(self, action):
        obs, self_rew, done, info = self.env.step(action)
        self.render()
        if done:
            info['winner'] = 'Agent'
            return obs, self_rew, done, info
        # Let other play
        action, _state = self.other_player.predict(obs)
        obs, rew, done, info = self.env.step(action)
        if done:
            if info['draw']:
                # Same reward for both
                reward = rew
                info['winner'] = 'Draw'
            else:
                # If the second won the game, give negative reward to the agent
                reward = -rew
                info['winner'] = 'Env'
        else:
            reward = self_rew
            info['winner'] = None
        return obs, reward, done, info

    def seed(self, seed):
        self.other_player.seed(seed)
        return [seed]

def make_env():
    from .env import QuartoEnv
    from .player import RandomPlayer, A2CPlayer
    env = QuartoEnv()
    #player = A2CPlayer('/home/ben/ML/quarto-gym/1PQuarto-v0.zip', env)
    player = RandomPlayer()
    env = OnePlayerWrapper(env, player)
    return env

register(
    id="1PQuarto-v0",
    entry_point="gym_quarto.wrapper:make_env",
    max_episode_steps=8,
)
