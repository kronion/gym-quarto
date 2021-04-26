import gym

from .game import QuartoPiece


class MoveEncoding(gym.ActionWrapper):
    """Move Encoding Wrapping

    Action is [x, y, big, hole, black, round]
    """

    def __init__(self, env: gym.Env) -> None:
        super(MoveEncoding, self).__init__(env)
        self.action_space = gym.spaces.MultiDiscrete([4, 4, 2, 2, 2, 2])

    def action(self, action):
        return self.decode(action)

    @property
    def legal_actions(self):
        for action in self.env.legal_actions:
            yield self.encode(action)

    def decode(self, action):
        position = (action[0], action[1])
        piece = QuartoPiece(
            action[2] * 1 + action[3] * 2 + action[4] * 4 + action[5] * 8
        )
        return position, piece

    def encode(self, move):
        position, piece = move
        return [
            position[0],
            position[1],
            int(piece.big),
            int(piece.hole),
            int(piece.black),
            int(piece.round),
        ]
