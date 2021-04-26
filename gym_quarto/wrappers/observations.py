from itertools import chain

import gym
import numpy as np


class ObsBoxEncoding(gym.ObservationWrapper):
    """
    Board encoding similar to the AlphaZero Chess Encoding

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
        super().__init__(env)

        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(4, 4, 4 + 1 + 4), dtype=np.int
        )

    def observation(self, obs):
        board, piece = obs

        res = np.zeros(shape=(4, 4, 4 + 1 + 4), dtype=np.int)
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
        return res


class ObsMultiDiscreteEncoding(gym.ObservationWrapper):
    """
    Represents the state as a numpy array of categoricals

    The board is a flattened array of categoricals representing pieces,
    and the choice of the next piece to play is appended to the end.
    """

    def __init__(self, env: gym.Env) -> None:
        super().__init__(env)

        # TODO handle magic numbers
        self.observation_space = gym.spaces.MultiDiscrete([17] * (1 + 4 * 4))

    def observation(self, obs):
        board, piece = obs

        # TODO handle magic numbers
        flattened_board = list(chain.from_iterable(self.game.board))
        flattened_board = [i.number if i is not None else 16 for i in flattened_board]
        piece = [self.piece.number if self.piece is not None else 16]
        return np.array(flattened_board + piece)
