from gym_quarto import QuartoEnv

env = QuartoEnv()

NB_EPISODE = 1
for episode in range(NB_EPISODE):
    env.reset()
    done = False
    while not done:
        action = stuff
        obs, reward, done, info = env.step(action)
        print(f"{info['turn']: <4} | ")
        env.render(fps=0.5)
    print("done")
env.close()

