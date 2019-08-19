import traceback
from pathlib import Path

import cv2
import numpy as np

from board import Board
from board_image import BoardImage
from square_status import SquareStatus

tmp_dir = Path("tmp")


def debug_imwrite(name, img):
    cv2.imwrite(str(tmp_dir / name), img)


def get_mask_by_bounds(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerb = (43, 69, 42)
    upperb = (87, 255, 255)

    mask = cv2.inRange(img_hsv, lowerb, upperb)
    return mask


def binarization_board_or_not(img):
    mask = get_mask_by_bounds(img)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return closed


def key_fn(t):
    return t[0]


def find_largest_contour(binary):
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    _, cnt = max([(cv2.contourArea(c), c) for c in contours], key=key_fn)
    return cnt


def get_board_contour(cnt):
    epsilon = 0.1 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    return approx


def projective_transformation(approx, img):
    # 画像の座標上から4角を切り出す
    pts1 = np.float32(approx)
    pts2 = np.float32([[0, 0], [0, 500], [500, 500], [500, 0]])

    # 透視変換の行列を求める
    M = cv2.getPerspectiveTransform(pts1, pts2)

    # 変換行列を用いて画像の透視変換
    return cv2.warpPerspective(img, M, (500, 500))


def get_color(img):
    disk_size_th = 1500
    mask = get_mask_by_bounds(img)
    debug_imwrite("square_mask.jpg", mask)
    disk = img[mask == 0]
    if disk.shape[0] < disk_size_th:
        return SquareStatus.EMPTY
    mean = np.mean(disk)
    if mean > 200:
        return SquareStatus.WHITE
    elif mean < 100:
        return SquareStatus.BLACK
    else:
        print("cannot judge color")
        print("mean: ", mean)
        return SquareStatus.EMPTY


def othello_board_recognition(img):
    binary = binarization_board_or_not(img)

    debug_imwrite("d1.jpg", binary)

    cnt = find_largest_contour(binary)
    d = img.copy()
    d = cv2.drawContours(d, [cnt], -1, (0, 0, 255), 5)
    debug_imwrite("d2.jpg", d)

    approx = get_board_contour(cnt)

    d = img.copy()
    d = cv2.drawContours(d, [approx], -1, (0, 0, 255), 5)
    debug_imwrite("d3.jpg", d)

    rst = projective_transformation(approx, img)

    debug_imwrite('d4.jpg', rst)
    # img = cv2.cvtColor(dst,cv2.COLOR_HSV2BGR)

    board = Board()
    for i in range(8):
        a = 500 // 8
        imin, imax = a * i, a * (i + 1) - 1
        for j in range(8):
            jmin, jmax = a * j, a * (j + 1) - 1
            square_img = rst[imin:imax, jmin:jmax]
            color = get_color(square_img)

            board[i, j] = color

            debug_imwrite(f"{i}_{j}.jpg", square_img)

    return board


def main():
    input_dir = Path("test")
    output_dir = Path("output")
    for img_path in input_dir.glob("*.jpg"):
        try:
            print("import: ", img_path)

            img = cv2.imread(str(img_path))

            board = othello_board_recognition(img)
            board_img = BoardImage(board)

            board_img.write(output_dir / img_path.name)
            # h, w, _ = img.shape
            # r_img = cv2.resize(img, (int(1024 * w / h), 1024))
            # result = cv2.hconcat([r_img, board_img._img])
            # cv2.imwrite(str(output_dir / img_path.name), result)
            # print(board)

        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    main()
