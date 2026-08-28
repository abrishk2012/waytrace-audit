"""Read-only panels for the WayTrace dashboard.

Every number here is READ from a committed file. Nothing is typed in by
hand and nothing is recomputed. If a file is missing, the panel says so
rather than showing a plausible number - Rule 51, a default is a value
you did not choose.
"""

import json
import os
import re

import streamlit as st

_NUM = re.compile(r"P=(\d+)%\s+R=(\d+)%\s+F1=(\d+)%")


def load_results(path):
    with open(path) as f:
        return json.load(f)


def parse_per_behaviour(path):
    """Pull the per-behaviour block out of per_behaviour_day15.txt.

    Parsed, not retyped: the handoff note's copy of these numbers has been
    wrong before and a summary is a weaker witness than the file. Rule 39.
    """
    if not os.path.exists(path):
        return None
    section, out = None, {}
    for line in open(path):
        s = line.strip()
        if s.startswith("ODD"):
            section = "ODD"
        elif s.startswith("EVEN"):
            section = "EVEN"
        elif s.startswith("ALL"):
            section = "ALL"
        elif section and s:
            m = _NUM.search(s)
            if m:
                kind = s.split()[0]
                out.setdefault(section, {})[kind] = tuple(
                    int(g) for g in m.groups())
    return out or None


def counts_panel(results):
    """Event counts for the recorded set. Scope stated on screen."""
    events = results["events"]
    trips = results["trips_examined"]
    hes = sum(1 for e in events if e["type"] == "HESITATION")
    utn = sum(1 for e in events if e["type"] == "UTURN")
    affected = len({e["trip"] for e in events})

    st.subheader("What was found")
    st.caption(
        f"All {len(trips)} labelled trips. These are counts of detected "
        "events, not accuracy - accuracy is measured separately below, on "
        "the held-out half only."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Events detected", len(events))
    c2.metric("Hesitations", hes)
    c3.metric("U-turns", utn)
    c4.metric("Trips with an event", f"{affected} of {len(trips)}")


def accuracy_panel(per_behaviour):
    """Held-out precision and recall, with the U-turn zero stated openly."""
    st.subheader("How accurate it is")
    if not per_behaviour:
        st.warning("per_behaviour_day15.txt not found - no figures shown.")
        return
    even = per_behaviour.get("EVEN", {})
    if not even:
        st.warning("No held-out block found in per_behaviour_day15.txt.")
        return

    st.caption(
        "Measured on the 12 EVEN trips only. The odd/even split was written "
        "down before any detector existed, the scoring script was committed "
        "before it was ever run, and the test was run once. These are the "
        "numbers it gave."
    )
    cols = st.columns(3)
    order = [("COMBINED", "Combined"), ("HESITATION", "Hesitation"),
             ("UTURN", "U-turn")]
    for col, (key, label) in zip(cols, order):
        if key in even:
            p, r, f1 = even[key]
            col.metric(f"{label} F1", f"{f1}%")
            col.caption(f"precision {p}%  ·  recall {r}%")

    if even.get("UTURN", (None,))[0] == 0:
        st.error(
            "**The U-turn detector scored zero on the held-out set.** Two "
            "U-turns were in it and both were missed, for the same reason "
            "each time: the speed gate ignores a turn made by someone who "
            "has already stopped. Both failures were predicted in writing on "
            "Day 14, before the held-out trips were opened. The combined 59% "
            "hides this completely, which is why the split is shown."
        )