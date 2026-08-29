import sys
import cv2
import numpy as np
IN = sys.argv[1]
OUT = sys.argv[2]
print("Undistorting:", IN, "->", OUT)

data = np.load("calibration_ezviz.npz")
K = data["K"]
dist = data["dist"]

cap = cv2.VideoCapture(IN)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
calib_w, calib_h = (int(v) for v in data["size"])
if (w, h) != (calib_w, calib_h):
    sys.exit(
        "REFUSING: video is %dx%d but calibration_ezviz.npz was made at %dx%d.\n"
        "A camera matrix is resolution-specific. Undistorting anyway would "
        "produce a plausible video with wrong metre coordinates."
        % (w, h, calib_w, calib_h)
    )

writer = cv2.VideoWriter(OUT, cv2.VideoWriter_fourcc(*"mp4v"), 15.0, (w, h))

count = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    writer.write(cv2.undistort(frame, K, dist))
    count += 1
    if count % 100 == 0:
        print("frame", count)

cap.release()
writer.release()
print("Done. Frames written:", count)