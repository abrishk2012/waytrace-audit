import cv2, numpy as np, glob

d = np.load("calibration_ezviz.npz")
K, dist = d["K"], d["dist"]
print("Calibrated at:", d["size"], "| RMS:", float(d["rms"]))

cap = cv2.VideoCapture("data/raw/2026-08-18_flat_calib.mp4")
cap.set(cv2.CAP_PROP_POS_FRAMES, 4000)
ok, frame = cap.read()
cap.release()
if not ok:
    raise SystemExit("Could not read that frame.")

fixed = cv2.undistort(frame, K, dist)
cv2.imwrite("data/output/undistort_check.jpg", np.hstack([frame, fixed]))
print("Saved data/output/undistort_check.jpg")