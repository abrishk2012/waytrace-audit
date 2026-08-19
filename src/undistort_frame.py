import cv2
import numpy as np

data = np.load("calibration_ezviz.npz")
K = data["K"]
dist = data["dist"]

img = cv2.imread("data/output/floor_raw.jpg")
if img is None:
    raise SystemExit("Could not read floor_raw.jpg")

print("Image size:", img.shape[1], "x", img.shape[0])

undistorted = cv2.undistort(img, K, dist)
cv2.imwrite("data/output/floor_undistorted.jpg", undistorted)
print("Saved data/output/floor_undistorted.jpg")