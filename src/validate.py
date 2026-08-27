"""Day 15 — score the LOCKED thresholds against the held-out set.

No sweeps. No tuning. No file writes. This script cannot change a threshold,
so it cannot be used to improve a number after seeing it.

The thresholds below were fixed on Day 13 against ODD trips only, committed
before any even trip was scored. Applying them unchanged to EVEN trips is what
"held-out" means.
"""
import sys
from tune import run
from odd_only import odd_trips, even_trips, all_trips

LOCKED = dict(max_speed=0.30, min_seconds=2.00, max_gap=0.00, window=5,
              min_angle=135.0, sustain=1.00, span_seconds=1.50, min_speed=0.20)

print("LOCKED THRESHOLDS (Day 13, committed before any even trip was scored)")
for k, v in LOCKED.items():
    print(f"  {k:<14}{v}")
print()

for label, fn, note in [
        ("ODD  (tuning set, 13 trips)",  odd_trips,  "self-check: must be 11/3/2, P=85% R=79%"),
        ("EVEN (HELD-OUT,   12 trips)",  even_trips, "*** THE REAL NUMBER ***"),
        ("ALL  (25 trips)",              all_trips,  "context only - includes the tuning set")]:
    h, m, f = run(**LOCKED, trips_fn=fn)
    p = h / (h + f) if h + f else 0.0
    r = h / (h + m) if h + m else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    print(f"{label}")
    print(f"  {h} hits  {m} misses  {f} false positives")
    print(f"  precision {p:.0%}   recall {r:.0%}   F1 {f1:.0%}")
    print(f"  {note}")
    print()

print("Whatever EVEN says is the honest number. It goes in the README as-is.")