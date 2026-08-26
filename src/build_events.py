"""Run both detectors over every clip and write one results.json.

This is the handover point between processing and display (the Day 1 decision).
Nothing downstream re-runs YOLO: the hotspot engine and the dashboard read this
file only, so a slow CPU can never break the demo.

Every event carries a POSITION as well as a time. An event without coordinates
cannot be clustered into a hotspot.
"""
import json, glob, os
import numpy as np
from speeds import (smooth, pixels_to_metres, drop_fragments,
                    find_hesitations, find_uturns, FPS)
import speeds

MAX_SPEED    = 0.3
MIN_SECONDS  = 2.0
MAX_GAP      = 1.0
WINDOW       = 5
MIN_ANGLE    = 135.0
SUSTAIN      = 1.0
SPAN_SECONDS = 1.5
MIN_SPEED    = 0.20

speeds.H = np.load("homography_camC.npz")["H"]


def position_at(world, t):
    """x, y in metres at time t seconds. Nearest stored point."""
    best, best_gap = world[0], 1e9
    for x, y, fr in world:
        gap = abs((fr - 1) / FPS - t)
        if gap < best_gap:
            best, best_gap = (x, y, fr), gap
    return round(float(best[0]), 3), round(float(best[1]), 3)


events = []
clips = sorted(glob.glob("data/output/*_traj.json"))
print(f"{len(clips)} clips found")

for path in clips:
    clip = os.path.basename(path).split("_")[-2]     # "clip1"
    with open(path) as f:
        tr = drop_fragments(json.load(f))

    n_trips = 0
    for tid, pts in tr.items():
        w = pixels_to_metres(pts)
        # A trip STARTS at the near end (y about -1); a walk-back starts at
        # the far end (y about +2). Judged by START position, not by net
        # displacement: a trip containing a U-turn ends where it began, so
        # 'final y > starting y' decides those on noise. Day 13: clip12
        # ID 19 rejected at -0.12 m, clip11 ID 1 accepted at +0.01 m.
        if w[0][1] > 0.5:
            continue                                  # walk-back, not a trip
        n_trips += 1

        for a, b, d in find_hesitations(w, max_speed=MAX_SPEED,
                                        min_seconds=MIN_SECONDS,
                                        max_gap=MAX_GAP, window=WINDOW):
            x, y = position_at(w, a)
            events.append({"clip": clip, "track_id": tid, "type": "HESITATION",
                           "start_sec": round(a, 1), "end_sec": round(b, 1),
                           "duration_sec": round(d, 1), "x_m": x, "y_m": y})

        for t, ang in find_uturns(w, min_angle=MIN_ANGLE, sustain=SUSTAIN,
                                  span_seconds=SPAN_SECONDS, window=WINDOW,
                                  min_speed=MIN_SPEED):
            x, y = position_at(w, t)
            events.append({"clip": clip, "track_id": tid, "type": "UTURN",
                           "start_sec": round(t, 1), "end_sec": round(t + 1, 1),
                           "duration_sec": 1.0, "x_m": x, "y_m": y})

    print(f"  {clip:>7}: {len(tr):2d} tracks, {n_trips} trips")

out = "data/output/results.json"
with open(out, "w") as f:
    json.dump({"thresholds": {"max_speed": MAX_SPEED, "min_seconds": MIN_SECONDS,
                              "max_gap": MAX_GAP, "window": WINDOW,
                              "min_angle": MIN_ANGLE, "sustain": SUSTAIN,
                              "span_seconds": SPAN_SECONDS,
                              "min_speed": MIN_SPEED},
               "events": events}, f, indent=2)

h = sum(1 for e in events if e["type"] == "HESITATION")
u = len(events) - h
print(f"\n{len(events)} events written to {out}  ({h} hesitations, {u} u-turns)")

