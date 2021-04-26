import gym

from ..game import QuartoPiece


class TwoChoiceEncoding(gym.ActionWrapper):
    """Move Encoding Wrapping

    Action is [location, piece]
    """

    def __init__(self, env: gym.Env) -> None:
        super().__init__(env)
        self.action_space = gym.spaces.MultiDiscrete([16, 16])

    def action(self, action):
        return self.decode(action)

    @property
    def legal_actions(self):
        for action in self.env.legal_actions:
            yield self.encode(action)

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

    def decode(self, action):
        position, next_piece = action
        if next_piece is not None:
            next_piece = QuartoPiece(next_piece)

        position = (position // 4, position % 4)
        return position, next_piece

    def encode(self, move):
        position, piece = move
        x, y = position
        return x * 4 + y, self.pieceNum(piece)
