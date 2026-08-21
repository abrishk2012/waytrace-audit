import json
import cv2
import numpy as np

FPS = 15.0
CM_PER_M = 100.0


# ============ FUNCTIONS ============

def smooth(points, window=5):
    """Moving average: replace each point with the average of itself
    and its neighbours. Kills random jitter, keeps real movement.
    Input and output are BOTH in METRES, as (x, y, frame).
    The frame number is NOT averaged - position gets smoothed, the clock does not."""
    half = window // 2
    out = []
    for i in range(len(points)):
        start = max(0, i - half)
        end   = min(len(points), i + half + 1)
        chunk = points[start:end]
        avg_x = sum(p[0] for p in chunk) / len(chunk)
        avg_y = sum(p[1] for p in chunk) / len(chunk)
        out.append((avg_x, avg_y, points[i][2]))
    return out


def trim_edges(world, seconds=0.7):
    """Drop the first and last N seconds of a track.
    Entry/exit box artefacts live there: the person is only half in frame,
    so the box shrinks and its bottom edge (the footpoint) lurches.
    That is the box moving, not the person."""
    if not world:
        return world
    first_f = world[0][2]
    last_f  = world[-1][2]
    cut = seconds * FPS          # seconds -> FRAMES. The list holds frame numbers.
    return [p for p in world
            if first_f + cut <= p[2] <= last_f - cut]


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


def y_swing(world, t0=18.3, t1=25.3):
    """Total up-down range in y during the known real movement."""
    ys = [y for x, y, f in world if t0 <= f / FPS <= t1]
    return max(ys) - min(ys)


# ============ LOAD ============
# Input is PIXELS (undistorted frame). Nothing is in cm yet.
with open("data/output/devwalk_trajectories.json") as f:
    trajectories = json.load(f)

print("Tracks loaded:", len(trajectories))
for track_id, points in trajectories.items():
    print(f"  ID {track_id}: {len(points)} points")
    print(f"    first point: {points[0]}")
    print(f"    last point:  {points[-1]}")

data = np.load("homography_camC.npz")
H = data["H"]
print()
print("Keys in homography_camC.npz:", list(data.keys()))


# ============ DISPLACEMENT CHECK, ALL THREE TRACKS ============
print()
for track_id, points in trajectories.items():
    wt = pixels_to_metres(points)
    dx = wt[-1][0] - wt[0][0]
    dy = wt[-1][1] - wt[0][1]
    dist = (dx**2 + dy**2) ** 0.5
    secs = (wt[-1][2] - wt[0][2]) / FPS
    print(f"ID {track_id}: dx={dx:+.2f} m  dy={dy:+.2f} m  "
          f"dist={dist:.2f} m  time={secs:.1f} s  avg={dist/secs:.2f} m/s")


# ============ ID 1 IN DETAIL ============
w = pixels_to_metres(trajectories["1"])

print()
print("ID 1, one row per second:")
for i in range(0, len(w), 15):
    x, y, f = w[i]
    print(f"  t={f/FPS:5.1f}s   x={x:+.2f}  y={y:+.2f}")

vals = [v for _, v in speeds_for(w)]
print()
print(f"ID 1 speed: min={min(vals):.2f}  max={max(vals):.2f}  "
      f"mean={sum(vals)/len(vals):.2f} m/s   ({len(vals)} samples)")


# ============ SMOOTHING SWEEP ============
print()
print("window   max speed   y-swing")
for win in (1, 3, 5, 9, 15):
    ws = smooth(w, window=win)
    vs = [v for _, v in speeds_for(ws)]
    print(f"  {win:2d}     {max(vs):.2f} m/s    {y_swing(ws):.2f} m")
print()
print("window=1 must equal unsmoothed. If it does not, smooth() has a bug.")


# ============ THE KNOWN 10-SECOND STOP ============
print()
print("ID 1, t=13-17s (the known 10-second stop):")
for win in (1, 5):
    ws = smooth(w, window=win)
    stop_vals = [v for f, v in speeds_for(ws) if 13.0 <= f/FPS <= 17.0]
    print(f"  window={win:2d}   max in stop={max(stop_vals):.2f} m/s   "
          f"mean={sum(stop_vals)/len(stop_vals):.2f} m/s")
print("  (walking speed is 0.64 m/s - these are uncomfortably close,")
print("   which is why the detector needs 'sustained for Y seconds')")


# ============ WHERE ARE THE SPIKES? ============
print()
sp = speeds_for(w)
worst = sorted(sp, key=lambda r: -r[1])[:5]
print("Top 5 fastest moments, UNSMOOTHED:")
for f, v in worst:
    print(f"  t={f/FPS:5.1f}s   {v:.2f} m/s")


# ============ WHICH AXIS? ============
print()
print("Which axis is the walk actually on?")
for track_id, points in trajectories.items():
    w2 = pixels_to_metres(points)
    dx = abs(w2[-1][0] - w2[0][0])
    dy = abs(w2[-1][1] - w2[0][1])
    print(f"  ID {track_id}:  |dx|={dx:.2f} m   |dy|={dy:.2f} m   "
          f"-> mostly {'X' if dx > dy else 'Y'}")


# ============ TRIM THE EDGES ============
print()
print("trim(s)   points   max speed")
for t in (0.0, 0.3, 0.5, 0.7, 1.0, 1.5):
    wt2 = trim_edges(w, seconds=t)
    vt = [v for _, v in speeds_for(wt2)]
    print(f"  {t:.1f}      {len(wt2):3d}      {max(vt):.2f} m/s")