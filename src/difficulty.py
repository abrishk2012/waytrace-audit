"""Do people hesitate more when their destination is not on the sign?

Joins the `dificulty` column of shoot_log.xlsx against event counts in
results.json and writes data/output/difficulty.json.

The labels were assigned AT FILMING TIME, before any detector existed, purely
by destination, and never edited afterwards. That is what makes this a
pre-registered comparison rather than a pattern found by digging through
results after the fact.

Row 0 of the sheet is a stray note about a robot vacuum (UNRESOLVED item 4),
so the header row is searched for, not assumed. The column is spelled
"dificulty" in the sheet; that spelling is authoritative here.

Run from the project root:
    python3 src/difficulty.py
"""
import json
from collections import defaultdict

import openpyxl

SHEET = "data/shoot_log.xlsx"
RESULTS = "data/output/results.json"
OUT = "data/output/difficulty.json"

rows = list(openpyxl.load_workbook(SHEET, data_only=True).worksheets[0]
            .iter_rows(values_only=True))

hdr = next(i for i, r in enumerate(rows)
           if r[0] is not None and str(r[0]).strip().lower() == "trip #")
cols = {str(c).strip().lower(): i for i, c in enumerate(rows[hdr]) if c}
print("header row", hdr, sorted(cols))

i_trip = cols["trip #"]
i_diff = cols["dificulty"]
i_dest = cols["destination card"]

label = {}
dest = {}
for r in rows[hdr + 1:]:
    if isinstance(r[i_trip], int) and r[i_diff]:
        label[r[i_trip]] = str(r[i_diff]).strip().upper()
        dest[r[i_trip]] = str(r[i_dest]).strip()

d = json.load(open(RESULTS))
assert d["scope"] == "ALL_TRIPS", d["scope"]

counts = defaultdict(int)
for e in d["events"]:
    counts[e["trip"]] += 1

gap = set(label) - {t["trip"] for t in d["trips_examined"]}
assert not gap, "trips in sheet but not examined: %s" % sorted(gap)

out = {"source_sheet": SHEET, "source_results": RESULTS, "groups": {}}
for g in ("EASY", "AMBIG", "MISSING"):
    trips = sorted(t for t in label if label[t] == g)
    ev = sum(counts[t] for t in trips)
    out["groups"][g] = {
        "trips": len(trips),
        "trip_ids": trips,
        "destinations": sorted({dest[t] for t in trips}),
        "events": ev,
        "events_per_trip": round(ev / len(trips), 3),
        "trips_with_any_event": sum(1 for t in trips if counts[t]),
    }

easy = out["groups"]["EASY"]["events_per_trip"]
miss = out["groups"]["MISSING"]["events_per_trip"]
out["missing_vs_easy_ratio"] = round(miss / easy, 2) if easy else None
out["caveats"] = [
    "n = %d MISSING trips. A direction, not a p-value."
    % out["groups"]["MISSING"]["trips"],
    "Some events are scored FALSE POSITIVE in data/misses_day15.txt.",
    "Clips 2, 4, 5 and 6 produced zero events and were never re-checked for "
    "missed events (UNRESOLVED item 5). Trip 9 (EASY) is in clip6, so the "
    "EASY rate is a floor.",
]

assert sum(v["trips"] for v in out["groups"].values()) == len(label)
json.dump(out, open(OUT, "w"), indent=2)

for g, v in out["groups"].items():
    print("%-8s trips=%2d events=%2d per_trip=%.2f any=%d/%d"
          % (g, v["trips"], v["events"], v["events_per_trip"],
             v["trips_with_any_event"], v["trips"]))
print("MISSING/EASY ratio:", out["missing_vs_easy_ratio"])
print("written to", OUT)
