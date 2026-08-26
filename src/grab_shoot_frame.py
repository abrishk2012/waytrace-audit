"""Grab one undistorted frame from a shoot clip, for locating fixed objects
like signage in world coordinates. Takes clip name and frame number."""
import cv2, sys, glob

clip = sys.argv[1] if len(sys.argv) > 1 else "clip1"
at   = int(sys.argv[2]) if len(sys.argv) > 2 else 30

src = glob.glob(f"data/undist/*{clip}.mp4")
if not src:
    raise SystemExit(f"no undistorted video for {clip}")
cap = cv2.VideoCapture(src[0])
out = f"data/output/{clip}_frame{at}.jpg"

n = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    if n == at:
        cv2.imwrite(out, frame)
        print(f"saved frame {at} to {out}")
        break
    n += 1
cap.release()
if n != at:
    print(f"WARNING: only {n} frames, never reached {at}")
