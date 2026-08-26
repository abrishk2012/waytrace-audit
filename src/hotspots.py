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
