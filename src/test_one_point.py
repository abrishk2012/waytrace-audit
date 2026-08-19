import cv2
import numpy as np

data = np.load("homography_camC.npz")
H = data["H"]

img = cv2.imread("data/output/floor_points.jpg")
if img is None:
    raise SystemExit("Could not read floor_points.jpg")

def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        p = np.array([[[float(x), float(y)]]], dtype=np.float32)
        out = cv2.perspectiveTransform(p, H)[0][0]
        print("Clicked pixel", x, y,
              "-> floor position", round(float(out[0]), 1),
              round(float(out[1]), 1), "cm")

cv2.namedWindow("Click any tile corner")
cv2.setMouseCallback("Click any tile corner", on_click)
cv2.imshow("Click any tile corner", img)
cv2.waitKey(0)
cv2.destroyAllWindows()