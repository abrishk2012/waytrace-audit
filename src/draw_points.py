import cv2
import numpy as np

data = np.load("homography_camC.npz")
image_points = data["image_points"]

img = cv2.imread("data/output/floor_undistorted.jpg")
if img is None:
    raise SystemExit("Could not read floor_undistorted.jpg")

pts = image_points.astype(int)

for i, (x, y) in enumerate(pts):
    cv2.circle(img, (x, y), 6, (0, 0, 255), -1)
    cv2.putText(img, str(i + 1), (x + 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

cv2.polylines(img, [pts.reshape(-1, 1, 2)], True, (0, 255, 0), 2)

cv2.imwrite("data/output/floor_points.jpg", img)
print("Saved data/output/floor_points.jpg")