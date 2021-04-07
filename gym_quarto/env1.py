import numpy as np

import gym


class MoveEncoding(gym.ActionWrapper):
    """Move Encoding Wrapping

    Action is [x, y, big, hole, black, round]
    """

    def __init__(self, env: gym.Env) -> None:
        super(MoveEncoding, self).__init__(env)
        self.action_space = gym.spaces.MultiDiscrete([4,4,2,2,2,2])

    def action(self, action):
        return self.decode(action)

    @property
    def legal_actions(self):
        for action in self.legal_actions:
            yield self.encode(action)

    def decode(self, action):
        position = (action[0], action[1])
        piece = QuartoPiece(
                x[2] * 1 + 
                x[3] * 2 + 
                x[4] * 4 + 
                x[5] * 8)
        return position, piece

    def encode(self, move):
        position, piece = move
        return [position[0], position[1],
                int(piece.big), int(piece.hole), int(piece.black), int(piece.round)]

class BoardEncoding(gym.ObservationWrapper):
    """Board encoding similar to the AlphaZero Chess Encoding

    See [Silver et al., 2017]

    The Board is observed as various layers, each one encoding a aspect of the
    pieces:
      - big
      - hole
      - black
      - round
      - taken

    The last four layers are about the shape of the next piece
      - big
      - hole
      - black
      - round
    """

    def __init__(self, env: gym.Env) -> None:
        super(BoardEncoding, self).__init__(env)

        self.observation_space = gym.spaces.Box(
            low=0, high=1,
            shape=(4,4,4+1+4),
            dtype=np.int
        )

    def observation(self, obs):
        print('called')
        board, piece = obs

        res = np.zeros(
            shape=(4, 4, 4+1+4),
            dtype=np.int
        )
        for y, row in enumerate(board):
            for x, piece in enumerate(row):
                if piece is not None:
                    res[x, y, 0] = int(piece.big)
                    res[x, y, 1] = int(piece.hole)
                    res[x, y, 2] = int(piece.black)
                    res[x, y, 3] = int(piece.round)
                    res[x, y, 4] = 1
        if piece is not None:
            res[:, :, 5] = int(piece.big)
            res[:, :, 6] = int(piece.hole)
            res[:, :, 7] = int(piece.black)
            res[:, :, 8] = int(piece.round)
        assert isinstance(res, np.ndarray)
        #print(f"returned {res}")
        return res
