import json, sys
import cv2
import numpy as np

FPS = 15.0
path = sys.argv[1]

with open(path) as f:
    tr = json.load(f)

H = np.load("homography_camC.npz")["H"]

print("Tracks in file:", len(tr))
print()
print("  ID   points   seconds   |dx| m   |dy| m   axis")
for tid, pts in sorted(tr.items(), key=lambda kv: -len(kv[1])):
    secs = (pts[-1][2] - pts[0][2]) / FPS
    ends = np.array([[[pts[0][0], pts[0][1]]],
                     [[pts[-1][0], pts[-1][1]]]], dtype=np.float32)
    w = cv2.perspectiveTransform(ends, H).reshape(-1, 2) / 100.0
    dx = abs(w[1][0] - w[0][0])
    dy = abs(w[1][1] - w[0][1])
    print(f"  {tid:>3}   {len(pts):6d}   {secs:7.1f}   {dx:6.2f}   {dy:6.2f}"
          f"   {'X' if dx > dy else 'Y'}")

short = sorted([t for t, p in tr.items() if len(p) < 15])
print()
print(f"Tracks under 1 second (15 points): {len(short)}  -> {short}")


print()
print("start/end y (metres), by track, in time order:")
rows = []
for tid, pts in tr.items():
    if len(pts) < 15:
        continue
    ends = np.array([[[pts[0][0], pts[0][1]]],
                     [[pts[-1][0], pts[-1][1]]]], dtype=np.float32)
    w = cv2.perspectiveTransform(ends, H).reshape(-1, 2) / 100.0
    rows.append(((pts[0][2] - 1) / FPS, tid, w[0][1], w[1][1]))
for t0, tid, y0, y1 in sorted(rows):
    print(f"  t={t0:6.1f}s  ID {tid:>3}   y {y0:+.2f} -> {y1:+.2f}   "
          f"{'DOWN (y falls)' if y1 < y0 else 'UP (y rises)'}")