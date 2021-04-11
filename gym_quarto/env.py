import logging
from itertools import chain

import gym
import numpy as np

from .game import QuartoGame, QuartoPiece

logger = logging.getLogger(__name__)


class QuartoEnv(gym.Env):
    EMPTY = 0
    metadata = {"render.modes": ["terminal"]}

    action_space = None
    observation_space = None

    def reset(self, random_start=True):
        self.game = QuartoGame()
        self.turns = 0
        self.piece = None
        self.broken = False
        return self._observation

    def step(self, action):
        reward = 0
        self.turns += 1
        info = {"turn": self.turns, "invalid": False, "win": False, "draw": False}
        if self.done:
            logger.warn("Actually already done")
            return self._observation, reward, self.done, info

        position, next = action
        logger.debug(f"Received: position: {position}, next: {next}")

        # Process the position
        if self.piece is not None:
            # Don't play on the first turn, just save the next piece
            valid = self.game.play(self.piece, position, next)
            if not valid:
                # Invalid move
                reward = -200
                self.broken = True
                info["invalid"] = True
            elif self.game.game_over:
                # We just won !
                reward = 100
                info["win"] = True
            elif self.game.draw:
                reward = 20
                info["draw"] = True
            else:
                # We managed to play something valid
                reward = 0

        # Process the next piece
        self.piece = next

        return self._observation, reward, self.done, info

    @property
    def _observation(self):
        """ game board + next piece
        """
        flattened_board = list(chain.from_iterable(self.game.board))
        flattened_board = [i.number if i is not None else 16 for i in flattened_board]
        piece = [self.piece.number if self.piece is not None else 16]
        return np.array(flattened_board + piece)

    @property
    def done(self):
        return self.broken or self.game.game_over or self.game.draw

    def render(self, mode, **kwargs):
        for row in self.game.board:
            s = ""
            for piece in row:
                if piece is None:
                    s += ". "
                else:
                    s += str(piece) + " "
            print(s)
        print(f"Next: {self.piece}, Free: {''.join(str(p) for p in self.game.free)}")
        print()

    @property
    def legal_actions(self):
        next_pieces = [p for p in self.game.free if p != self.piece]
        if len(next_pieces) == 0:
            next_pieces = [None]

        for position in self.game.free_spots:
            for piece in next_pieces:
                yield position, piece

    @staticmethod
    def action_mask_fn(env) -> np.ndarray:
        mask = []
        for row in env.game.board:
            for pos in row:
                if pos is None:
                    mask.append(True)
                else:
                    mask.append(False)
        for piece in env.game.pieces:
            if piece in env.game.free and piece != env.piece:
                mask.append(True)
            else:
                mask.append(False)

        return np.array(mask)

        # mask = [self._valid_action(action) for action in self.actions]
        # return np.array(mask)

    def action_masks(self) -> np.ndarray:
        return self.action_mask_fn(self)

    @staticmethod
    def pieceNum(piece):
        if piece is None:
            return 16

        res = 0
        if piece.big:
            res += 1
        if piece.hole:
            res += 2
        if piece.black:
            res += 4
        if piece.round:
            res += 8
        return res

    @staticmethod
    def pieceFromStr(s):
        for i in range(16):
            if str(QuartoPiece(i)) == s:
                return i
        return None

    def __del__(self):
        self.close()


class QuartoEnvV0(QuartoEnv):
    """ The encoding that were used by the v0 of the env
    That's a subclass and not a wrapper.
    """

    def __init__(self):
        super(QuartoEnvV0, self).__init__()

        # next piece + board (flatten)
        self.observation_space = gym.spaces.MultiDiscrete([17] * (1 + 4 * 4))

        # action is [pos, next]
        # both are not null, they are just ignored when irrelevant
        self.action_space = gym.spaces.MultiDiscrete([16, 16])

    def step(self, action):
        position, next = action
        if next is not None:
            next = QuartoPiece(next)
        position = (position // 4, position % 4)
        return super(QuartoEnvV0, self).step((position, next))

    @property
    def observation(self):
        board = []
        for row in self.game.board:
            for piece in row:
                if piece is None:
                    board.append(self.EMPTY)
                else:
                    board.append(QuartoEnv.pieceNum(piece) + 1)
        if self.piece is None:
            piece = [self.EMPTY]
        else:
            piece = [QuartoEnv.pieceNum(self.piece) + 1]
        return np.concatenate((piece, board)).astype(np.int8)

    @property
    def legal_actions(self):
        for position, piece in super(QuartoEnvV0, self).legal_actions:
            x, y = position
            yield x * 4 + y, QuartoEnv.pieceNum(piece)
