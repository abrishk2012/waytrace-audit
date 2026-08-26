"""Hesitation detector v1.
Thresholds come from docs/definitions.md, NOT from tuning.
0.3 m/s, 2.0 s. These are expected to be wrong. Day 13 tunes them, ODD trips only.
"""
import json, sys
import numpy as np
from speeds import (smooth, speeds_for, pixels_to_metres,
                    drop_fragments, find_hesitations, find_uturns, FPS)
import speeds

MAX_SPEED   = 0.3    # definitions.md
MIN_SECONDS = 2.0    # definitions.md
MAX_GAP     = 1.0    # not in definitions.md - see note below
WINDOW      = 5      # locked on Day 8
MIN_ANGLE     = 135.0   # definitions.md
SUSTAIN       = 1.0     # definitions.md
SPAN_SECONDS  = 1.5     # implementation choice, not in definitions.md

path = sys.argv[1]
with open(path) as f:
    tr = json.load(f)

speeds.H = np.load("homography_camC.npz")["H"]

tr = drop_fragments(tr)
print(f"{len(tr)} tracks after fragment filter")

trips = {}
for tid, pts in tr.items():
    w = pixels_to_metres(pts)
    if w[-1][1] > w[0][1]:          # definitions.md: trip = final y > start y
        trips[tid] = w
print(f"{len(trips)} of those run in the trip direction (rest are walk-backs)")
print()

for tid, w in sorted(trips.items(), key=lambda kv: kv[1][0][2]):
    t0 = (w[0][2] - 1) / FPS
    hes = find_hesitations(w, max_speed=MAX_SPEED, min_seconds=MIN_SECONDS,
                           max_gap=MAX_GAP, window=WINDOW)
    utn = find_uturns(w, min_angle=MIN_ANGLE, sustain=SUSTAIN,
                      span_seconds=SPAN_SECONDS, window=WINDOW)
    print(f"ID {tid:>3}  starts t={t0:6.1f}s   "
          f"{len(hes)} hesitation(s), {len(utn)} u-turn(s)")
    for a, b, d in hes:
        print(f"        HESITATION  {a:6.1f}s to {b:6.1f}s   ({d:.1f}s)")
    for t, ang in utn:
        print(f"        UTURN       {t:6.1f}s   {ang:5.1f} degrees")

    if len(sys.argv) > 2:
        tid = sys.argv[2]
        w = trips[tid]
        speed_at = {fr: v for fr, v in speeds_for(smooth(w, window=WINDOW))}
        print()
        print("speed and heading change, one row per 0.5 s:")
        from speeds import heading
        ws = smooth(w, window=WINDOW)
        span = int(SPAN_SECONDS * FPS)
        hold = int(SUSTAIN * FPS)
        for i in range(0, len(ws), 7):
            t = (ws[i][2] - 1) / FPS
            b = heading(ws, i, span)
            a = heading(ws, min(i + hold, len(ws) - 1), span)
            v = speed_at.get(ws[i][2])
            if b is None or a is None or v is None:
                continue
            d = abs(a - b)
            if d > 180:
                d = 360 - d
            print(f"  t={t:6.1f}s   speed={v:5.2f} m/s   turn={d:6.1f} deg")
