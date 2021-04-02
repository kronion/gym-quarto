import gym
import logging
import numpy as np
import random

from gym.envs.registration import register

from .game import QuartoGame, QuartoPiece

logger = logging.getLogger(__name__)

class QuartoEnv(gym.Env):
    EMPTY = 0
    metadata = {'render.modes':['terminal']}

    def __init__(self):
        super(QuartoEnv, self).__init__()

        # action is [pos, next]
        # both are not null, they are just ignored when irrelevant
        self.action_space = gym.spaces.MultiDiscrete([16, 16])

        # next piece + board (flatten) 
        self.observation_space = gym.spaces.MultiDiscrete([17] * (1+4*4))

        self.reset()

    def reset(self, random_start=True):
        self.game = QuartoGame()
        self.turns = 0
        self.piece = None
        self.broken = False
        return self.observation

    def step(self, action):
        reward = 0
        self.turns += 1
        info = {'turn': self.turns,
                'invalid': False,
                'win': False,
                'draw': False}
        if self.done:
            logger.warn("Actually already done")
            return self.observation, reward, self.done, info

        position, next = action
        logger.debug(f"Received: position: {position}, next: {next}")
        if next is not None:
            next = QuartoPiece(next)

        # Process the position
        if self.piece is not None:
            # Don't play on the first turn, just save the next piece
            valid = self.game.play(self.piece, (position % 4, position // 4), next)
            if not valid:
                # Invalid move
                reward = -200
                self.broken = True
                info['invalid'] = True
            elif self.game.game_over:
                # We just won !
                reward = 100
                info['win'] = True
            elif self.game.draw:
                reward = 20
                info['draw'] = True
            else:
                # We managed to play something valid
                reward = 0

        # Process the next piece
        self.piece = next

        return self.observation, reward, self.done, info

    @property
    def observation(self):
        """ game board + next piece
        """
        board = []
        for row in self.game.board:
            for piece in row:
                if piece is None:
                    board.append(self.EMPTY)
                else:
                    board.append(QuartoEnv.pieceNum(piece) + 1)
        if self.piece is None:
            piece = [self.EMPTY]
        else :
            piece = [QuartoEnv.pieceNum(self.piece) + 1]
        return np.concatenate((piece, board)).astype(np.int8)

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

    @staticmethod
    def pieceNum(piece):
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

register(
    id='quarto-v0',
    entry_point='gym_quarto.env:QuartoEnv',
    max_episode_steps=16,
)
