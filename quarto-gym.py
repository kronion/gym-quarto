import gym

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


class QuartoGame(object):

    def __init__(self):
        self.board = [[None for i in range(4)] for i in range(4)]
        self.free = [QuartoPiece(i) for i in range(16)]

    def play(self, piece, position) -> boolean:
        # check if piece in self.free
        if piece not in self.free:
            return False
        # check if position free
        x, y = position
        if self.board[y][x] != None:
            return False
        # position piece
        self.board[y][x] = piece
        # remove from free
        self.free.remove(piece)

    def game_over(self):
        for i in range(4):
            if QuartoGame.common(self.board[i][0], self.board[i][1], self.board[i][2], self.board[i][3]):
                return True
            if QuartoGame.common(self.board[0][i], self.board[1][i], self.board[2][i], self.board[3][i]):
                return True
        if QuartoGame.common(self.board[0][0], self.board[1][1], self.board[2][2], self.board[3][3]):
            return True
        if QuartoGame.common(self.board[0][3], self.board[1][2], self.board[2][1], self.board[3][0]):
            return True
        return False


    @staticmethod
    def common(a, b, c, d):
        if None in (a, b, c, d):
            return False
        if a.big == b.big == c.big == d.big:
            return True
        if a.hole == b.hole == c.hole == d.hole:
            return True
        if a.black == b.black == c.black == d.black:
            return True
        if a.round == b.round == c.round == d.round:
            return True
        return False



class QuartoPiece(object):
    """ A piece in the game of quarto
    """
    def __init__(self, number):
        self.big = number & 0x1
        self.hole = number & 0x2
        self.black = number & 0x4
        self.round = number & 0x8

    def __eq__(self, other):
        return isinstance(other, QuartoPiece) and self.big == other.big and self.hole == other.hole and self.black == other.black and self.round == other.round

    @property
    def id(self):
        return 

