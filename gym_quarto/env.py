import gym

from .game import QuartoGame, QuartoPiece

class QuartoEnv(gym.Env):
    metadata = {'render.modes':['terminal']}

    def __init__(self):
        super(QuartoEnv, self).__init__()

        # action is [pos, next]
        self.action_space = gym.spaces.Box(
                low =0, high=16, shape=(2,), dtype=np.uint8)


        self.reset()

    def reset(selfi, random_start=True):
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
