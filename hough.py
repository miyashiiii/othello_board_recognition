import cv2
import numpy as np

img = cv2.imread("test/IMG_9932.jpg")


def get_mask_by_bounds(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerb = (43, 69, 42)
    upperb = (87, 255, 255)

    mask = cv2.inRange(img_hsv, lowerb, upperb)
    return mask


mask = get_mask_by_bounds(img)
mask = cv2.bitwise_not(mask)
cv2.imwrite("d1.jpg", mask)
edges = cv2.Canny(mask, 50, 150, apertureSize=3)

lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
for rho, theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 5)

cv2.imwrite("d.jpg", img)
