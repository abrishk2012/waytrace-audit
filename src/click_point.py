"""Click ONE floor point, get its position in metres.

For locating fixed objects - signage, doors - in the same coordinates as the
events. Click the FLOOR directly below the object, never the object itself:
the homography maps the floor plane only, so a point up a wall is placed as if
it were lying flat (same reason trajectories use the box bottom, not centre).
"""
import cv2, sys
import numpy as np

img_path = sys.argv[1]
H = np.load("homography_camC.npz")["H"]

img = cv2.imread(img_path)
if img is None:
    raise SystemExit("could not read " + img_path)
disp = img.copy()

def on_click(event, x, y, flags, param):
    if event != cv2.EVENT_LBUTTONDOWN:
        return
    p = np.array([[[float(x), float(y)]]], dtype=np.float32)
    w = cv2.perspectiveTransform(p, H).reshape(2) / 100.0
    print(f"pixel ({x}, {y})  ->  x={w[0]:+.2f} m   y={w[1]:+.2f} m")
    cv2.circle(disp, (x, y), 5, (0, 0, 255), -1)
    cv2.putText(disp, f"{w[0]:+.2f},{w[1]:+.2f}", (x + 8, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.imshow("click the FLOOR below the object", disp)

cv2.namedWindow("click the FLOOR below the object")
cv2.setMouseCallback("click the FLOOR below the object", on_click)
cv2.imshow("click the FLOOR below the object", disp)
print("Click the floor point. Press any key to finish.")
cv2.waitKey(0)
cv2.destroyAllWindows()
