import json
import cv2
import numpy as np

FPS = 15.0
CM_PER_M = 100.0


# ============================================================
#  FUNCTIONS
#  Everything below the functions is running code.
#  A function must be DEFINED above the line that calls it.
# ============================================================

def smooth(points, window=5):
    """Moving average: replace each point with the average of itself
    and its neighbours. Kills random jitter, keeps real movement.
    Input and output are BOTH in METRES, as (x, y, frame).
    The frame number is NOT averaged - position is smoothed, the clock is not."""
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


def trim_edges(world, seconds=0.5):
    """Drop the first and last N seconds of a track.
    NOTE: proven on Day 8.5 to help only ID 1. No common trim value exists
    across tracks. Kept as a mild guard, not as the fix it was hoped to be."""
    if not world:
        return world
    first_f = world[0][2]
    last_f  = world[-1][2]
    cut = seconds * FPS          # seconds -> FRAMES. The list holds frame numbers.
    return [p for p in world
            if first_f + cut <= p[2] <= last_f - cut]


def find_hesitations(world, max_speed=0.25, min_seconds=1.5,
                     max_gap=1.0, window=5):
    """Find periods below max_speed lasting at least min_seconds.

    max_gap is the point of this function. A brief excursion above the
    threshold does NOT end the event, because standing still is not zero
    speed - people shift weight, turn, look around. Without gap tolerance
    one real 10-second stop fragments into two or three false short ones.

    Returns list of (start_time, end_time, duration) in seconds."""
    sp = speeds_for(smooth(world, window=window))

    events = []
    run_start = None
    last_slow = None
    for f, v in sp:
        t = f / FPS
        if v < max_speed:
            if run_start is None:
                run_start = t
            last_slow = t
        else:
            # only close the event if we have been fast for LONGER than max_gap
            if run_start is not None and t - last_slow > max_gap:
                if last_slow - run_start >= min_seconds:
                    events.append((run_start, last_slow, last_slow - run_start))
                run_start = None
    # a track can end mid-hesitation - without this the last event is lost
    if run_start is not None and last_slow - run_start >= min_seconds:
        events.append((run_start, last_slow, last_slow - run_start))
    return events


# ---- THE ONE AND ONLY UNIT CONVERSION ----
# H maps pixels -> CENTIMETRES (see Day 5 notes).
# Everything downstream of this function is in METRES.
def pixels_to_metres(points):
    """points: list of [x, y, frame, ...] in pixels.
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


# ============================================================
#  LOAD
# ============================================================
# Input is PIXELS (undistorted frame). Nothing is in cm yet.
with open("data/output/devwalk_trajectories.json") as f:
    trajectories = json.load(f)

print("Tracks loaded:", len(trajectories))
for track_id, points in trajectories.items():
    print(f"  ID {track_id}: {len(points)} points")

n_vals = len(next(iter(trajectories.values()))[0])
print(f"Values per point: {n_vals}",
      "(x, y, frame)" if n_vals == 3 else "(x, y, frame, box_w, box_h)")

data = np.load("homography_camC.npz")
H = data["H"]


# ============================================================
#  DISPLACEMENT CHECK, ALL THREE TRACKS
# ============================================================
print()
for track_id, points in trajectories.items():
    wt = pixels_to_metres(points)
    dx = wt[-1][0] - wt[0][0]
    dy = wt[-1][1] - wt[0][1]
    dist = (dx**2 + dy**2) ** 0.5
    secs = (wt[-1][2] - wt[0][2]) / FPS
    print(f"ID {track_id}: dx={dx:+.2f} m  dy={dy:+.2f} m  "
          f"dist={dist:.2f} m  time={secs:.1f} s  avg={dist/secs:.2f} m/s")
print("(hand-measured answer key: 2.46 m. Reported 2.44 m = 3 cm agreement)")


# ============================================================
#  ID 1 IN DETAIL
# ============================================================
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


# ============================================================
#  SMOOTHING SWEEP    window=5 is LOCKED
# ============================================================
print()
print("window   max speed   y-swing")
for win in (1, 3, 5, 9, 15):
    ws = smooth(w, window=win)
    vs = [v for _, v in speeds_for(ws)]
    print(f"  {win:2d}     {max(vs):.2f} m/s    {y_swing(ws):.2f} m")
print("  window=1 MUST equal unsmoothed (3.70 / 1.74). If not, smooth() is broken.")
print("  Chose 5 over 9/15: bigger windows blur event START and END in time.")


# ============================================================
#  THE KNOWN 10-SECOND STOP
# ============================================================
print()
print("ID 1, t=13-17s (confirmed standstill):")
for win in (1, 5):
    ws = smooth(w, window=win)
    stop_vals = [v for f, v in speeds_for(ws) if 13.0 <= f/FPS <= 17.0]
    print(f"  window={win:2d}   max in stop={max(stop_vals):.2f} m/s   "
          f"mean={sum(stop_vals)/len(stop_vals):.2f} m/s")
print("  Walking is 0.64 m/s. Standing peaks at 0.49. The two OVERLAP,")
print("  which is why no bare speed threshold can separate them.")


# ============================================================
#  HESITATION DETECTION
# ============================================================
print()
print("ID 1 GROUND TRUTH: one stop, 7.3s to 17.3s (10.0s)")
print()
print("max_gap   n   events")
for g in (0.0, 0.5, 1.0, 1.5, 2.0, 3.0):
    ev = find_hesitations(w, max_gap=g)
    desc = "  ".join(f"{a:.1f}-{b:.1f}" for a, b, d in ev)
    print(f"  {g:.1f}     {len(ev)}   {desc}")
print("  max_gap=0.0 is the null row: it must reproduce the 2-event result.")

print()
print("All tracks, max_gap=1.0:")
for tid in ("1", "6", "8"):
    ww = pixels_to_metres(trajectories[tid])
    ev = find_hesitations(ww, max_gap=1.0)
    if not ev:
        print(f"  ID {tid}: none")
    for a, b, d in ev:
        print(f"  ID {tid}:  {a:.1f}s to {b:.1f}s   ({d:.1f}s)")


# ============================================================
#  DIAGNOSTICS - five hypotheses for the residual speed spikes
#  Four rejected, one supported. Kept as evidence, not as live code.
# ============================================================
print()
print("Top 5 fastest moments, ID 1, UNSMOOTHED:")
for f, v in sorted(speeds_for(w), key=lambda r: -r[1])[:5]:
    print(f"  t={f/FPS:5.1f}s   {v:.2f} m/s")

print()
print("Which axis is the walk on? (README claimed y - it is x)")
for track_id, points in trajectories.items():
    w2 = pixels_to_metres(points)
    dx = abs(w2[-1][0] - w2[0][0])
    dy = abs(w2[-1][1] - w2[0][1])
    print(f"  ID {track_id}:  |dx|={dx:.2f} m   |dy|={dy:.2f} m   "
          f"-> mostly {'X' if dx > dy else 'Y'}")

print()
print("REJECTED hypothesis: time-based trimming (works on ID 1 only)")
print("trim   ID1     ID6     ID8")
for t in (0.0, 0.7, 1.0, 1.5, 2.0, 2.5, 3.0):
    row = []
    for tid in ("1", "6", "8"):
        ww = trim_edges(pixels_to_metres(trajectories[tid]), seconds=t)
        vv = [v for _, v in speeds_for(ww)]
        row.append(f"{max(vv):.2f}" if vv else "  - ")
    print(f"  {t:.1f}   {row[0]}    {row[1]}    {row[2]}")
print("  ID 6 never flattens - it just erodes. No common boundary exists.")

print()
print("SUPPORTED hypothesis: position. cm covered by ONE pixel:")
for py in (150, 250, 350, 450, 550):
    pts = np.array([[[500, py]], [[501, py]], [[500, py+1]]], dtype=np.float32)
    wp = cv2.perspectiveTransform(pts, H).reshape(-1, 2)
    across = np.linalg.norm(wp[1] - wp[0])
    along  = np.linalg.norm(wp[2] - wp[0])
    print(f"  image row y={py:4d}  ->  1px = {across:.2f} cm across, {along:.2f} cm along")
print("  0.40 cm near the camera, 1.68 cm far away = 4.2x spread.")
print("  Same detector jitter is worth 4x the metres at the far end.")
print("  The three biggest spikes all occur at world y = +1.49 to +1.53.")