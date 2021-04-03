import logging

logger = logging.getLogger(__name__)

class QuartoGame(object):

    def __init__(self):
        self.board = [[None for i in range(4)] for i in range(4)]
        self.free = [QuartoPiece(i) for i in range(16)]

    def play(self, piece, position, next_piece) -> bool:
        # check if piece in self.free
        if piece not in self.free:
            logger.warn(f"Not placing a free piece, {piece}, {''.join(str(p) for p in self.free)}")
            return False
        # check if position free
        x, y = position
        logger.debug(f"Willing to play at ({x}, {y})")
        if self.board[y][x] != None:
            logger.warn(f"Not on a free spot {self.board[y][x]} at {x}, {y}")
            return False
        # position piece
        self.board[y][x] = piece
        # remove from free
        self.free.remove(piece)
        if not self.game_over and next_piece not in self.free:
            logger.warn(f"Next piece invalid, {next_piece}, {''.join(str(p) for p in self.free)}")
            return False
        return True

    @property
    def game_over(self):
        for i in range(4):
            if QuartoGame.common(self.board[i][0], self.board[i][1], self.board[i][2], self.board[i][3]):
                logger.info(f" y = {i}, done")
                return True
            if QuartoGame.common(self.board[0][i], self.board[1][i], self.board[2][i], self.board[3][i]):
                logger.info(f" x = {i}, done")
                return True
        if QuartoGame.common(self.board[0][0], self.board[1][1], self.board[2][2], self.board[3][3]):
            logger.info("top-left, bottom-right, done")
            return True
        if QuartoGame.common(self.board[0][3], self.board[1][2], self.board[2][1], self.board[3][0]):
            logger.info("top-right, bottom-left, done")
            return True
        return False

    @property
    def draw(self):
        """ Game is finished but no one won
        """
        for row in self.board:
            if None in row:
                # Free spot: no draw
                return False
        # No free spot, no win: draw
        return not self.game_over

    @property
    def free_spots(self):
        for y, row in enumerate(self.board):
            for x, spot in enumerate(row):
                if spot is None:
                    yield x, y


    @staticmethod
    def common(a, b, c, d):
        """ The four piece have a common property
        """
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
        self.big = bool(number & 0x1)
        self.hole = bool(number & 0x2)
        self.black = bool(number & 0x4)
        self.round = bool(number & 0x8)

    def __eq__(self, other):
        return isinstance(other, QuartoPiece) and (
            self.big == other.big and
            self.hole == other.hole and
            self.black == other.black and
            self.round == other.round)
        
    def __str__(self):
        return {
            (False, False, False, False): 'A',
            (False, False, False, True): 'B',
            (False, False, True, False): 'C',
            (False, False, True, True): 'D',
            (False, True, False, False): 'E',
            (False, True, False, True): 'F',
            (False, True, True, False): 'G',
            (False, True, True, True): 'H',
            (True, False, False, False): 'a',
            (True, False, False, True): 'b',
            (True, False, True, False): 'c',
            (True, False, True, True): 'd',
            (True, True, False, False): 'e',
            (True, True, False, True): 'f',
            (True, True, True, False): 'g',
            (True, True, True, True): 'h',
        }[self.big, self.hole, self.black, self.round]

