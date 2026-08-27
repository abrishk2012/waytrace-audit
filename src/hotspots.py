"""Cluster events into wayfinding friction hotspots.

One hesitation is a person. Six hesitations in one spot is a hotspot.

Reads results_odd.json (or results.json with --all on Day 15). Never re-runs
YOLO or the detectors - the Day 1 processing/display split.

Clustering is grid-based, not DBSCAN: the corridor is 3 m long and the whole
dataset is tens of events, so a grid is easier to explain to a judge and has
one parameter instead of two. CELL_M is the only knob.
"""
import json, sys, collections

CELL_M = 0.5     # grid cell size in metres
MIN_EVENTS = 2   # a cell needs this many events to count as a hotspot

ALL = "--all" in sys.argv
path = "data/output/results.json" if ALL else "data/output/results_odd.json"
d = json.load(open(path))
print(f"scope: {d['scope']}   {len(d['events'])} events")

cells = collections.defaultdict(list)
for e in d["events"]:
    key = (round(e["x_m"] / CELL_M), round(e["y_m"] / CELL_M))
    cells[key].append(e)

hotspots = []
for (cx, cy), evs in cells.items():
    if len(evs) < MIN_EVENTS:
        continue
    types = collections.Counter(e["type"] for e in evs)
    hotspots.append({
        "x_m": round(cx * CELL_M, 2),
        "y_m": round(cy * CELL_M, 2),
        "event_count": len(evs),
        "hesitations": types["HESITATION"],
        "uturns": types["UTURN"],
        "trips_affected": sorted(set(e["trip"] for e in evs)),
        "mean_confidence": round(sum(e["confidence"] for e in evs) / len(evs), 2),
    })

hotspots.sort(key=lambda h: -h["event_count"])

out = "data/output/hotspots.json" if ALL else "data/output/hotspots_odd.json"
with open(out, "w") as f:
    json.dump({"scope": d["scope"], "cell_m": CELL_M,
               "min_events": MIN_EVENTS, "hotspots": hotspots}, f, indent=2)

print()
print(f"{len(cells)} occupied cells, {len(hotspots)} hotspots "
      f"(>= {MIN_EVENTS} events in a {CELL_M} m cell)")
print()
print(f"{'x_m':>6} {'y_m':>6} {'n':>3} {'hes':>4} {'utn':>4}  trips")
for h in hotspots:
    print(f"{h['x_m']:6.2f} {h['y_m']:6.2f} {h['event_count']:3d} "
          f"{h['hesitations']:4d} {h['uturns']:4d}  {h['trips_affected']}")
print()
print(f"written to {out}")

print()
print("CELL_M sensitivity - the clustering is only as stable as this table:")
for cm in (0.3, 0.4, 0.5, 0.6, 0.75, 1.0):
    cc = collections.defaultdict(list)
    for e in d["events"]:
        cc[(round(e["x_m"] / cm), round(e["y_m"] / cm))].append(e)
    hs = [v for v in cc.values() if len(v) >= MIN_EVENTS]
    covered = sum(len(v) for v in hs)
    print(f"  cell={cm:.2f} m   {len(cc):2d} cells   {len(hs)} hotspots   "
          f"{covered}/{len(d['events'])} events clustered")

# ---- SIGNAGE AUDIT ----
# "possible signage issue associated with this hotspot", never "this sign
# caused it". The system measures distance, not causation.
import math
try:
    signs = json.load(open("data/signs.json"))["signs"]
except Exception as err:
    signs = []
    print("no signs.json:", err)

if signs and hotspots:
    print()
    print("distance from each hotspot to the nearest sign:")
    for h in hotspots:
        best, best_d = None, 1e9
        for s in signs:
            dist = math.hypot(h["x_m"] - s["x_m"], h["y_m"] - s["y_m"])
            if dist < best_d:
                best, best_d = s, dist
        h["nearest_sign"] = best["id"]
        h["distance_to_sign_m"] = round(best_d, 2)
        kind = ("u-turn dominated" if h["uturns"] > h["hesitations"]
                else "hesitation dominated" if h["hesitations"] > h["uturns"]
                else "mixed")
        print(f"  ({h['x_m']:+.2f}, {h['y_m']:+.2f})  {h['event_count']} events, "
              f"{kind:<20} {best_d:.2f} m from {best['id']}")
        print(f"      sign reads: {', '.join(best['text'])}")
        print(f"      absent from sign: {', '.join(best['absent'])}")

    with open(out, "w") as f:
        json.dump({"scope": d["scope"], "cell_m": CELL_M,
                   "min_events": MIN_EVENTS, "hotspots": hotspots}, f, indent=2)
    print()
    print(f"{out} rewritten with sign distances")

# ---- PIPELINE SANITY CHECK (Day 14) ----
# Junction geometry is measured from the BUILDING, never from detector output.
# If the biggest hotspot does not land near the junction, something upstream is
# wrong even when every number looks reasonable.
try:
    junc = json.load(open("data/signs.json"))["junction"]
except Exception:
    junc = None

if junc and hotspots:
    jx, jy = junc["centre_x_m"], junc["centre_y_m"]
    print()
    print(f"junction centre ({jx:+.2f}, {jy:+.2f}) from "
          f"{len(junc['openings'])} measured openings")
    sides = []
    for i, h in enumerate(hotspots, 1):
        dj = math.hypot(h["x_m"] - jx, h["y_m"] - jy)
        h["distance_to_junction_m"] = round(dj, 2)
        approach = h["y_m"] < jy
        h["side"] = "approach" if approach else "beyond"
        sides.append(approach)
        side = "approach side" if approach else "beyond the junction"
        print(f"  hotspot {i}: {dj:.2f} m from junction, {side}")
    with open(out, "w") as f:
        json.dump({"scope": d["scope"], "cell_m": CELL_M,
                   "min_events": MIN_EVENTS, "hotspots": hotspots}, f, indent=2)
    if all(sides):
        print(f"  SANITY CHECK PASSED - all {len(sides)} hotspots on the approach side")
    else:
        bad = [i for i, s in enumerate(sides, 1) if not s]
        print(f"  *** SANITY CHECK FAILED *** hotspot(s) {bad} beyond the junction")
        print("  *** People do not hesitate after choosing. Suspect the homography,")
        print("  *** the junction measurement, or the trip direction filter.")