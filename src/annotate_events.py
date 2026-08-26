"""Burn detected events onto a clip's video.

Reads results_odd.json only - never re-runs YOLO. This is the display half of the
Day 1 processing/display split: the demo cannot be broken by a slow CPU because
nothing is computed here.
"""
import json, sys, os, glob
import cv2
import numpy as np

clip = sys.argv[1] if len(sys.argv) > 1 else "clip1"
FPS = 15.0

d = json.load(open("data/output/results_odd.json"))
events = [e for e in d["events"] if e["clip"] == clip]
print(f"{len(events)} events in {clip}")

src = glob.glob(f"data/undist/*{clip}.mp4") or glob.glob(f"data/cfr/*{clip}.mp4")
if not src:
    print("!! no source video found for", clip)
    sys.exit(1)
src = src[0]
print("reading", src)

H = np.load("homography_camC.npz")["H"]
H_inv = np.linalg.inv(H)

def to_pixels(x_m, y_m):
    """Metres back to pixels, so a marker lands where the person was."""
    p = np.array([[[x_m * 100.0, y_m * 100.0]]], dtype=np.float32)
    q = cv2.perspectiveTransform(p, H_inv).reshape(2)
    return int(q[0]), int(q[1])

cap = cv2.VideoCapture(src)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out_path = f"data/output/{clip}_events.mp4"
out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"), FPS, (w, h))

frame_no = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame_no += 1
    t = (frame_no - 1) / FPS

    for e in events:
        if not (e["start_sec"] <= t <= e["end_sec"] + 1.0):
            continue
        px, py = to_pixels(e["x_m"], e["y_m"])
        colour = (0, 165, 255) if e["type"] == "HESITATION" else (0, 0, 255)
        cv2.circle(frame, (px, py), 40, colour, 3)
        cv2.putText(frame, f'{e["type"]} {e["confidence"]:.2f}',
                    (px - 60, py - 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, colour, 2)

    cv2.putText(frame, f"t={t:5.1f}s", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    out.write(frame)

cap.release()
out.release()
print(f"{frame_no} frames written to {out_path}")
