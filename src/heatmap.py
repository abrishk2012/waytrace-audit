"""Draw hotspots, signage and junction geometry onto a still frame.

The picture for the README and the opening of the demo video.
Reads hotspots_odd.json and signs.json. Computes nothing - pure drawing.

TEXT: one putText call on an optional dark plate. Day 14 spent hours on a
two-pass outline (thick black stroke, then thin coloured fill) which ghosted
every letter. text_test.py proved a SINGLE putText renders perfectly at every
size, so the doubling came from the two passes - not the font, not the viewer.
"""
import json, sys, glob, math
import cv2
import numpy as np

clip = sys.argv[1] if len(sys.argv) > 1 else "clip13"
ALL = "--all" in sys.argv

hs_path = "data/output/hotspots.json" if ALL else "data/output/hotspots_odd.json"
d = json.load(open(hs_path))
cfg = json.load(open("data/signs.json"))
signs = cfg["signs"]
junc = cfg.get("junction")
print(f"scope: {d['scope']}   {len(d['hotspots'])} hotspots   {len(signs)} signs")

frame_path = glob.glob(f"data/output/{clip}_frame*.jpg")
if not frame_path:
    raise SystemExit(f"no frame image for {clip}")
img = cv2.imread(frame_path[0])
print("drawing on", frame_path[0])

H = np.load("homography_camC.npz")["H"]
H_inv = np.linalg.inv(H)


def to_px(x_m, y_m):
    p = np.array([[[x_m * 100.0, y_m * 100.0]]], dtype=np.float32)
    q = cv2.perspectiveTransform(p, H_inv).reshape(2)
    return int(q[0]), int(q[1])


def label(im, text, x, y, colour, scale=0.55, box=True):
    """ONE putText, on an optional dark plate. Never two passes."""
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, 1)
    if box:
        cv2.rectangle(im, (int(x) - 5, int(y) - th - 5),
                      (int(x) + tw + 5, int(y) + 6), (22, 22, 22), -1)
    cv2.putText(im, text, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
                scale, colour, 1, cv2.LINE_AA)


def circle_pos(h):
    """ONE source for position, radius and clipped flag - fill and outline
    both call this. Day 14 bug: they each computed their own and drifted."""
    px, py = to_px(h["x_m"], h["y_m"])
    r = 26 + 9 * h["event_count"]
    clipped = py + r > img.shape[0] - 6
    if clipped:
        py = img.shape[0] - r - 8
    return px, py, r, clipped


def colour_for(h):
    return (0, 0, 255) if h["uturns"] > h["hesitations"] else (0, 165, 255)


overlay = img.copy()
for h in d["hotspots"]:
    px, py, r, _ = circle_pos(h)
    cv2.circle(overlay, (px, py), r, colour_for(h), -1)
cv2.addWeighted(overlay, 0.38, img, 0.62, 0, img)

if junc:
    for o in junc["openings"]:
        px, py = to_px(o["x_m"], o["y_m"])
        cv2.drawMarker(img, (px, py), (170, 255, 170),
                       cv2.MARKER_TILTED_CROSS, 18, 2)

ranked = sorted(d["hotspots"], key=lambda k: -k["event_count"])
for i, h in enumerate(ranked, 1):
    px, py, r, clipped = circle_pos(h)
    cv2.circle(img, (px, py), r, colour_for(h), 3)
    label(img, str(i), px - 9, py + 10, (255, 255, 255), 0.9, box=False)
    if clipped:
        label(img, "below frame edge", px - 58, py + r + 16,
              (235, 235, 235), 0.42, box=False)

for s in signs:
    px, py = to_px(s["x_m"], s["y_m"])
    cv2.drawMarker(img, (px, py), (255, 255, 0), cv2.MARKER_TRIANGLE_UP, 26, 3)
    label(img, s["id"], px - 20, py + 26, (255, 255, 0), 0.45, box=False)

label(img, f'WayTrace  |  {len(d["hotspots"])} friction hotspots  |  {d["scope"]}',
      14, 30, (255, 255, 255), 0.58)

py_panel = 62
for i, h in enumerate(ranked, 1):
    c = colour_for(h)
    kind = "u-turns" if h["uturns"] > h["hesitations"] else "hesitations"
    label(img, f'{i}.  {h["event_count"]} events, mostly {kind}', 40, py_panel, c, 0.52)
    cv2.circle(img, (25, py_panel - 5), 8, c, -1)
    bits = [f'{h["hesitations"]} hes / {h["uturns"]} u-turn']
    if h.get("distance_to_sign_m") is not None:
        bits.append(f'{h["distance_to_sign_m"]} m from sign')
    if h.get("distance_to_junction_m") is not None:
        bits.append(f'{h["distance_to_junction_m"]} m from junction')
    label(img, "    " + "  |  ".join(bits), 40, py_panel + 21, c, 0.44)
    label(img, f'    trips {h["trips_affected"]}', 40, py_panel + 40, c, 0.44)
    py_panel += 62

hgt = img.shape[0]
s0 = signs[0]
label(img, "SIGN READS:   " + "    ".join(s0["text"]), 14, hgt - 62, (255, 255, 0), 0.52)
label(img, "NOT ON SIGN:  " + ", ".join(s0["absent"]), 14, hgt - 40, (255, 255, 255), 0.52)
if junc:
    label(img, f'{len(junc["openings"])} openings at the junction (green crosses)',
          14, hgt - 18, (170, 255, 170), 0.46)

out = "data/output/heatmap.png" if ALL else "data/output/heatmap_odd.png"
cv2.imwrite(out, img)
print("written to", out)