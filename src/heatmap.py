"""Draw hotspots and signage onto a still frame - the picture for the README
and the opening of the demo video.

Reads hotspots_odd.json and signs.json. Computes nothing: the Day 1
processing/display split means this is pure drawing.
"""
import json, sys, glob
import cv2
import numpy as np

clip = sys.argv[1] if len(sys.argv) > 1 else "clip1"
ALL = "--all" in sys.argv

hs_path = "data/output/hotspots.json" if ALL else "data/output/hotspots_odd.json"
d = json.load(open(hs_path))
signs = json.load(open("data/signs.json"))["signs"]
print(f"scope: {d['scope']}   {len(d['hotspots'])} hotspots   {len(signs)} signs")

frame_path = glob.glob(f"data/output/{clip}_frame*.jpg")
if not frame_path:
    raise SystemExit(f"no frame image for {clip} - run grab_shoot_frame.py first")
img = cv2.imread(frame_path[0])
print("drawing on", frame_path[0])

H = np.load("homography_camC.npz")["H"]
H_inv = np.linalg.inv(H)

def to_px(x_m, y_m):
    p = np.array([[[x_m * 100.0, y_m * 100.0]]], dtype=np.float32)
    q = cv2.perspectiveTransform(p, H_inv).reshape(2)
    return int(q[0]), int(q[1])

def label(im, text, x, y, colour, scale=0.62):
    """Outlined text. The outline and the fill MUST use identical coordinates
    or the two passes read as doubled letters."""
    cv2.putText(im, text, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
                scale, (0, 0, 0), 4)
    cv2.putText(im, text, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
                scale, colour, 1, cv2.LINE_AA)


overlay = img.copy()
for h in d["hotspots"]:
    px, py = to_px(h["x_m"], h["y_m"])
    colour = (0, 0, 255) if h["uturns"] > h["hesitations"] else (0, 165, 255)
    cv2.circle(overlay, (px, py), 25 + 12 * h["event_count"], colour, -1)
cv2.addWeighted(overlay, 0.35, img, 0.65, 0, img)

# Labels are stacked BELOW each circle and alternate side to side, because on
# Day 14 the first version put them all above and the sign caption ran straight
# through them.
# Labels live in a fixed panel, not floating by the circles. Day 14: the two
# hotspots sit close together near the bottom edge, so floating labels either
# overlapped each other or fell off the frame. A panel cannot collide.
panel_y = 58
for i, h in enumerate(sorted(d["hotspots"], key=lambda k: -k["event_count"])):
    px, py = to_px(h["x_m"], h["y_m"])
    r = 25 + 12 * h["event_count"]
    colour = (0, 0, 255) if h["uturns"] > h["hesitations"] else (0, 165, 255)
    cv2.circle(img, (px, py), r, colour, 3)
    label(img, str(i + 1), px - 8, py + 9, (255, 255, 255), 0.9)
    cv2.circle(img, (26, panel_y - 6), 9, colour, -1)
    label(img, f'{i+1}.  {h["event_count"]} events, {h.get("distance_to_sign_m","?")} m from sign',
          42, panel_y, colour, 0.55)
    label(img, f'     {h["hesitations"]} hesitation / {h["uturns"]} u-turn, '
               f'trips {h["trips_affected"]}', 42, panel_y + 22, colour, 0.48)
    panel_y += 50
for s in signs:
    px, py = to_px(s["x_m"], s["y_m"])
    cv2.drawMarker(img, (px, py), (255, 255, 0), cv2.MARKER_TRIANGLE_UP, 28, 3)
    label(img, s["id"], px - 18, py + 24, (255, 255, 0), 0.5)

# Sign caption goes bottom-left, away from every circle.
hgt = img.shape[0]
s0 = signs[0]
label(img, "SIGN READS:  " + "   ".join(s0["text"]), 14, hgt - 44, (255, 255, 0), 0.5)
label(img, "NOT ON SIGN: " + ", ".join(s0["absent"]), 14, hgt - 24, (255, 255, 255), 0.5)

label(img, f'WayTrace - {len(d["hotspots"])} friction hotspots - {d["scope"]}',
      14, 28, (255, 255, 255), 0.6)

out = "data/output/heatmap.png" if ALL else "data/output/heatmap_odd.png"
cv2.imwrite(out, img)
print("written to", out)



