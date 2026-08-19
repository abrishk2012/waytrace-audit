import cv2, numpy as np

d = np.load("calibration_ezviz.npz")
K, dist = d["K"], d["dist"]

cap = cv2.VideoCapture("data/raw/fisheye_test.mp4")
cap.set(cv2.CAP_PROP_POS_FRAMES, 8)
ok, img = cap.read()
cap.release()
if not ok:
    raise SystemExit("Could not read frame.")

h, w = img.shape[:2]
if (w, h) != tuple(d["size"]):
    raise SystemExit(f"Frame is {w}x{h}, calibration is for {tuple(d['size'])}. Stop.")

fixed = cv2.undistort(img, K, dist)
cv2.imwrite("data/output/fisheye_before_after.jpg", np.hstack([img, fixed]))
print("Saved data/output/fisheye_before_after.jpg")