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