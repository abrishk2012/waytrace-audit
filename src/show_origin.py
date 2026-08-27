"""Draw the four tile-diamond calibration corners on a real frame.
Reads image_points and world_points straight from homography_camC.npz, so what
you see is exactly what the homography was fitted to - not a re-derivation.
Writes to a DEBUG filename. Rule 44: never write to a real output path."""
import cv2, sys, glob, numpy as np

clip = sys.argv[1] if len(sys.argv) > 1 else "clip1"
at   = int(sys.argv[2]) if len(sys.argv) > 2 else 30

d = np.load("homography_camC.npz")
img_pts, wrl_pts = d["image_points"], d["world_points"]

src = glob.glob(f"data/undist/*{clip}.mp4")
if not src:
    raise SystemExit(f"no undistorted video for {clip}")

cap = cv2.VideoCapture(src[0])
frame, n = None, 0
while True:
    ok, f = cap.read()
    if not ok:
        break
    if n == at:
        frame = f
        break
    n += 1
cap.release()
if frame is None:
    raise SystemExit(f"only {n} frames, never reached {at}")

pts = img_pts.astype(int)
cv2.polylines(frame, [pts.reshape(-1, 1, 2)], True, (0, 200, 255), 2)

for i, ((px, py), (wx, wy)) in enumerate(zip(pts, wrl_pts)):
    origin = (wx == 0 and wy == 0)
    colour = (0, 0, 255) if origin else (0, 200, 255)
    cv2.circle(frame, (px, py), 9, colour, -1)
    cv2.circle(frame, (px, py), 9, (255, 255, 255), 2)
    label = f"{i}: ({wx:.0f},{wy:.0f})cm" + ("  <-- ORIGIN (0,0)" if origin else "")
    cv2.putText(frame, label, (px + 14, py - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 4)
    cv2.putText(frame, label, (px + 14, py - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, colour, 2)

cv2.putText(frame, "x = short side 58.8cm    y = long side 154cm down the corridor",
            (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
cv2.putText(frame, "x = short side 58.8cm    y = long side 154cm down the corridor",
            (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

out = f"data/output/DEBUG_origin_{clip}_f{at}.jpg"
cv2.imwrite(out, frame)
print("wrote", out)