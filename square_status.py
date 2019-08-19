from enum import Enum


class SquareStatus(Enum):
    EMPTY = "EMPTY"
    BLACK = "BLACK"
    WHITE = "WHITE"

    def __str__(self):
        return self.value
