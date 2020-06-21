# 선수를 enum으로 표현
from collections import namedtuple
import enum

class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

class Point(namedtuple('Point', 'row col')):
    def neightbors(self):
        return [
            Point(self.row -1, self.col),
            Point(self.row +1, self.col),
            Point(self.row, self.col -1),
            Point(self.row, self.col +1),
        ]

