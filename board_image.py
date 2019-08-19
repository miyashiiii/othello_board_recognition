import cv2
import numpy as np

from square_status import SquareStatus


class BoardImage:
    board_color = np.array([0, 100, 0], dtype=np.uint8)
    board_size = 1024
    line_color = [0, 0, 0]
    black_color = [0, 0, 0]
    white_color = [255, 255, 255]
    line_bold = 3
    board_point_radius = 9

    def __init__(self, board=None):

        self.square_size = self.board_size // 8
        img = np.zeros((self.board_size, self.board_size, 3), dtype=np.uint8)
        img += self.board_color

        for i in range(9):
            i *= self.square_size
            img = cv2.line(img, (i, 0), (i, self.board_size), self.line_color, self.line_bold)
            img = cv2.line(img, (0, i), (self.board_size, i), self.line_color, self.line_bold)

        circle_indices = [
            (self.square_size * 2, self.square_size * 2),
            (self.square_size * 6, self.square_size * 2),
            (self.square_size * 2, self.square_size * 6),
            (self.square_size * 6, self.square_size * 6),
        ]

        for idx in circle_indices:
            img = cv2.circle(img, idx, self.board_point_radius, self.line_color, -1)

        self._img = img
        if board is not None:
            self.import_board(board)

    def _index_varidation(self, key):
        try:
            x, y = key
        except TypeError:
            raise TypeError("index must be 2 values")

        if x < 0 or 7 < x or y < 0 or 7 < y:
            raise IndexError(f"index must be 0 to 7. got x: {x}, y:{y}.")
        return x, y

    def get_disk_color(self, status):
        if status == SquareStatus.BLACK:
            return self.black_color
        elif status == SquareStatus.WHITE:
            return self.white_color
        else:
            raise ValueError("color must be black or white")

    def __setitem__(self, key, status):
        x, y = self._index_varidation(key)
        self.draw(x, y, status)

    def draw(self, x, y, status):

        if not isinstance(status, SquareStatus):
            raise TypeError("color must be Color")

        disk_radius = int(self.square_size * 0.45)
        circle_x, circle_y = int(self.square_size * (0.5 + x)), int(self.square_size * (0.5 + y))
        if status != SquareStatus.EMPTY:
            color = self.get_disk_color(status)
            self._img = cv2.circle(self._img, (circle_y, circle_x), disk_radius, color, -1)

    def import_board(self, board):
        for i in range(8):
            for j in range(8):
                self.draw(i, j, board[i, j])

    def write(self, path):
        cv2.imwrite(str(path), self._img)


if __name__ == "__main__":
    board_img = BoardImage()
    board_img.write("1.jpg")
    board_img[3, 4] = SquareStatus.BLACK
    board_img.write("2.jpg")
