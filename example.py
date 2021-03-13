import logging
import random

from stable_baselines3.common.env_checker import check_env

from gym_quarto import QuartoEnv, OnePlayerWrapper, RandomPlayer, random_action

logging.basicConfig(level=logging.INFO)

env = QuartoEnv()
env = OnePlayerWrapper(env, RandomPlayer())

#check_env(env)

NB_EPISODE = 1
for episode in range(NB_EPISODE):
    obs = env.reset()
    done = False
    while not done:
        action = random_action(env.game, obs[0])
        obs, reward, done, info = env.step(action)
        #print(f"{info['turn']: <4} | ")
        env.render()
    print("done")
env.close()

