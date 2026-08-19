import cv2
import numpy as np

image_points = np.array([
    [399, 431],
    [473, 536],
    [755, 374],
    [668, 306],
], dtype=np.float32)

world_points = np.array([
    [0.0,  0.0],
    [58.8, 0.0],
    [58.8, 154.0],
    [0.0,  154.0],
], dtype=np.float32)

H, mask = cv2.findHomography(image_points, world_points)

if H is None:
    raise SystemExit("findHomography failed")

print("Homography matrix:")
print(H)

np.savez("homography_camC.npz", H=H,
         image_points=image_points,
         world_points=world_points)
print()
print("Saved homography_camC.npz")