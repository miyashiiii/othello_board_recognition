from square_status import SquareStatus


class Board:

    def __init__(self):
        empty = SquareStatus.EMPTY
        self._board = [
            [empty, empty, empty, empty, empty, empty, empty, empty, ],
            [empty, empty, empty, empty, empty, empty, empty, empty, ],
            [empty, empty, empty, empty, empty, empty, empty, empty, ],
            [empty, empty, empty, empty, empty, empty, empty, empty, ],
            [empty, empty, empty, empty, empty, empty, empty, empty, ],
            [empty, empty, empty, empty, empty, empty, empty, empty, ],
            [empty, empty, empty, empty, empty, empty, empty, empty, ],
            [empty, empty, empty, empty, empty, empty, empty, empty, ],
        ]

    def _index_varidation(self, x, y):

        if x < 0 or 7 < x or y < 0 or 7 < y:
            raise IndexError(f"index must be 0 to 7. got x: {x}, y:{y}.")

    def __setitem__(self, key, status):
        try:
            x, y = key
        except TypeError:
            raise TypeError("index must be 2 values")

        self._index_varidation(x, y)

        if not isinstance(status, SquareStatus):
            raise TypeError("color must be Color")

        self._board[x][y] = status

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._board[key]
        elif isinstance(key, tuple):
            try:
                x, y = key
            except TypeError:
                raise TypeError("index must be 2 values")

            self._index_varidation(x, y)

            return self._board[x][y]

    def __str__(self):
        return "".join([str([status.value for status in row]) + "\n" for row in self._board])
