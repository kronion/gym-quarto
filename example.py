import logging
import random

import gym
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import A2C

from gym_quarto import QuartoEnvV0, OnePlayerWrapper, RandomPlayer, HumanPlayer, random_action

logging.basicConfig(level=logging.INFO)

def make_env(player=None):
    env = gym.make('quarto-v1')
    if player is None:
        player = RandomPlayer(env)
    env = OnePlayerWrapper(env, player)
    return env

check_env(make_env())

def random_vs_random():
    env = make_env()
    NB_EPISODE = 1
    for episode in range(NB_EPISODE):
        obs = env.reset()
        done = False
        while not done:
            action = random.choice(list(env.legal_actions))
            obs, reward, done, info = env.step(action)
            #print(f"{info['turn']: <4} | ")
            env.render()
        print("done")
    
def a2c(path):
    env = make_env(HumanPlayer())

    eval_env = make_env(RandomPlayer())


    model= A2C.load(path, env, verbose=1)

    mean, std = evaluate_policy(model, eval_env, n_eval_episodes=10)
    print(f"Loaded policy: mean={mean:.2f} +/- {std}")
    # Show how well we learned by plating a game:
    obs = env.reset()
    done = False
    while not done:
        action, _state = model.predict(obs)
        obs, reward, done, info = env.step(action)
        print(f"{info['turn']: <4} | Reward: {reward: >4} | {info['winner']}")
        env.render()
    print("done")

import sys
#a2c(sys.argv[1])

def random_vs_human():
    env = make_env()
    human = HumanPlayer()
    NB_EPISODE = 1
    for episode in range(NB_EPISODE):
        obs = env.reset()
        env.render()
        done = False
        while not done:
            action, _state = human.predict(obs)
            obs, reward, done, info = env.step(action)
            print(f"{info['turn']: <4} | Reward: {reward: >4}")
            env.render()
        print("done")

random_vs_random()
