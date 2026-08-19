import cv2
import numpy as np

data = np.load("homography_camC.npz")
H = data["H"]
image_points = data["image_points"]
world_points = data["world_points"]

def to_floor(x, y):
    p = np.array([[[float(x), float(y)]]], dtype=np.float32)
    out = cv2.perspectiveTransform(p, H)
    return out[0][0]

print("TEST 1 — do the 4 clicks map back to what we told it?")
for i in range(4):
    px, py = image_points[i]
    got = to_floor(px, py)
    want = world_points[i]
    print("  point", i + 1,
          "-> got", np.round(got, 2),
          "| expected", want)