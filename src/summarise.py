"""Which trips did the system examine, and what did it find in each?
A trip with zero events and a trip never seen look identical in results_odd.json.
Day 15 must not confuse them (Rule 38)."""
import json, collections

d = json.load(open("data/output/results_odd.json"))
ev = collections.defaultdict(list)
for e in d["events"]:
    ev[(e["clip"], e["track_id"])].append(e)

print("thresholds:", json.dumps(d["thresholds"]))
print()
print(f"{'clip':>7}  {'track':>5}  {'hes':>3} {'utn':>3}")
for key in sorted(ev, key=lambda k: (k[0], int(k[1]))):
    h = sum(1 for e in ev[key] if e["type"] == "HESITATION")
    u = sum(1 for e in ev[key] if e["type"] == "UTURN")
    print(f"{key[0]:>7}  {key[1]:>5}  {h:3d} {u:3d}")

print()
print(f"{len(ev)} trips produced events, {len(d['events'])} events total")
