import json
import cv2
import numpy as np

FPS = 15.0
CM_PER_M = 100.0

# ---- LOAD ----
# Input is PIXELS (undistorted frame). Nothing is in cm yet.
with open("data/output/devwalk_trajectories.json") as f:
    trajectories = json.load(f)

print("Tracks loaded:", len(trajectories))
for track_id, points in trajectories.items():
    print(f"  ID {track_id}: {len(points)} points")
    print(f"    first point: {points[0]}")
    print(f"    last point:  {points[-1]}")

# ---- HOMOGRAPHY ----
data = np.load("homography_camC.npz")
H = data["H"]
print()
print("Keys in homography_camC.npz:", list(data.keys()))


# ---- THE ONE AND ONLY UNIT CONVERSION ----
# H maps pixels -> CENTIMETRES (see Day 5 notes).
# Everything downstream of this function is in METRES.
def pixels_to_metres(points):
    """points: list of [x, y, frame] in pixels.
       returns: list of (x_m, y_m, frame) in METRES."""
    pts = np.array([[p[0], p[1]] for p in points], dtype=np.float32)
    pts = pts.reshape(-1, 1, 2)
    world_cm = cv2.perspectiveTransform(pts, H).reshape(-1, 2)
    return [(x / CM_PER_M, y / CM_PER_M, points[i][2])
            for i, (x, y) in enumerate(world_cm)]


# ---- PER-FRAME SPEED (m/s) ----
# Input is already METRES. No division by 100 anywhere below this line, ever.
def speeds_for(world):
    """world: list of (x_m, y_m, frame). returns list of (frame, speed_m_s)."""
    out = []
    for i in range(1, len(world)):
        x0, y0, f0 = world[i - 1]
        x1, y1, f1 = world[i]
        gap = (f1 - f0) / FPS          # seconds between the two points
        if gap <= 0:
            continue
        step = ((x1 - x0)**2 + (y1 - y0)**2) ** 0.5
        out.append((f1, step / gap))
    return out


# ---- DISPLACEMENT CHECK, ALL THREE TRACKS ----
print()
for track_id, points in trajectories.items():
    w = pixels_to_metres(points)
    dx = w[-1][0] - w[0][0]
    dy = w[-1][1] - w[0][1]
    dist = (dx**2 + dy**2) ** 0.5
    secs = (w[-1][2] - w[0][2]) / FPS
    print(f"ID {track_id}: dx={dx:+.2f} m  dy={dy:+.2f} m  "
          f"dist={dist:.2f} m  time={secs:.1f} s  avg={dist/secs:.2f} m/s")

# ---- WHERE DID THE TIME GO? sample ID 1 every 15 frames (1 second) ----
w = pixels_to_metres(trajectories["1"])
print()
print("ID 1, one row per second:")
for i in range(0, len(w), 15):
    x, y, f = w[i]
    print(f"  t={f/FPS:5.1f}s   x={x:+.2f}  y={y:+.2f}")

# ---- SPEED SUMMARY ----
vals = [v for _, v in speeds_for(w)]
print()
print(f"ID 1 speed: min={min(vals):.2f}  max={max(vals):.2f}  "
      f"mean={sum(vals)/len(vals):.2f} m/s   ({len(vals)} samples)")