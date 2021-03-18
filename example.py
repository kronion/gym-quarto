import logging
import random

from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import A2C

from gym_quarto import QuartoEnv, OnePlayerWrapper, RandomPlayer, random_action

logging.basicConfig(level=logging.INFO)

def make_env():
    env = QuartoEnv()
    env = OnePlayerWrapper(env, RandomPlayer())
    return env

#check_env(env)

def random_vs_random():
    env = make_env()
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
    
def a2c():
    env = make_env()
    model = A2C('MlpPolicy', env, verbose = 1)

    eval_env = make_env()
    mean, std = evaluate_policy(model, eval_env, n_eval_episodes=10)
    s = f"before learning mean={mean:.2f} +/- {std}"

    model.learn(total_timesteps=10_000_000)

    mean, std = evaluate_policy(model, eval_env, n_eval_episodes=10)
    print(s)
    print(f"after learning mean={mean:.2f} +/- {std}")
    # Show how well we learned by plating a game:
    obs = env.reset()
    done = False
    while not done:
        action, _state = model.predict(obs)
        obs, reward, done, info = env.step(action)
        #print(f"{info['turn']: <4} | ")
        env.render()
    print("done")

a2c()