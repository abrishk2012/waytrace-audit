"""Run the detectors on ONE unlabelled video's trajectories.

For dashboard uploads. No trip.csv, no odd/even guard - there are no held-out
labels to protect on footage that has never been labelled. build_events.py is
NOT touched: it stays exactly as it was on Day 15.

Same detectors, same locked thresholds, imported from speeds.py. Rule 42.
"""
import json, os, sys
import numpy as np
from speeds import (pixels_to_metres, drop_fragments,
                    find_hesitations, find_uturns, FPS)
import speeds

MAX_SPEED    = 0.30
MIN_SECONDS  = 2.00
MAX_GAP      = 0.00
WINDOW       = 5
MIN_ANGLE    = 135.0
SUSTAIN      = 1.00
SPAN_SECONDS = 1.50
MIN_SPEED    = 0.20

speeds.H = np.load("homography_camC.npz")["H"]


def to_json_safe(v):
    """numpy float32 -> python float, at the ONE point data leaves the maths
    and enters the file. Duplicated from build_events.py on purpose, not by
    accident: build_events.py produced the validated results.json on Day 15
    and is deliberately frozen, so nothing imports from it."""
    return float(v)


def position_at(world, t):
    best, gap_best = world[0], 1e9
    for x, y, fr in world:
        gap = abs((fr - 1) / FPS - t)
        if gap < gap_best:
            best, gap_best = (x, y, fr), gap
    return round(to_json_safe(best[0]), 3), round(to_json_safe(best[1]), 3)


def analyse(traj_path):
    with open(traj_path) as f:
        tracks = drop_fragments(json.load(f))

    events = []
    for tid, pts in tracks.items():
        w = pixels_to_metres(pts)
        if w[0][1] > 0.5:
            continue

        for a, b, d in find_hesitations(w, max_speed=MAX_SPEED,
                                        min_seconds=MIN_SECONDS,
                                        max_gap=MAX_GAP, window=WINDOW):
            x, y = position_at(w, a)
            events.append({"track_id": tid, "type": "HESITATION",
                           "start_sec": round(a, 1), "end_sec": round(b, 1),
                           "duration_sec": round(d, 1), "x_m": x, "y_m": y,
                           "confidence": round(min(1.0, d / MIN_SECONDS), 2)})

        for t, ang in find_uturns(w, min_angle=MIN_ANGLE, sustain=SUSTAIN,
                                  span_seconds=SPAN_SECONDS, window=WINDOW,
                                  min_speed=MIN_SPEED):
            x, y = position_at(w, t)
            events.append({"track_id": tid, "type": "UTURN",
                           "start_sec": round(t, 1), "end_sec": round(t + 1, 1),
                           "duration_sec": 1.0, "x_m": x, "y_m": y,
                           "angle_deg": round(to_json_safe(ang), 1),
                           "confidence": 1.0})

    events.sort(key=lambda e: e["start_sec"])
    return {"scope": "UNLABELLED", "source": os.path.basename(traj_path),
            "tracks_examined": len(tracks),
            "thresholds": {"max_speed": MAX_SPEED, "min_seconds": MIN_SECONDS,
                           "max_gap": MAX_GAP, "window": WINDOW,
                           "min_angle": MIN_ANGLE, "sustain": SUSTAIN,
                           "span_seconds": SPAN_SECONDS,
                           "min_speed": MIN_SPEED},
            "events": events}


if __name__ == "__main__":
    traj_path = sys.argv[1]
    out_path = sys.argv[2]
    result = analyse(traj_path)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"{result['tracks_examined']} tracks, {len(result['events'])} events")
    print("Saved to", out_path)