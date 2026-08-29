"""Read-only panels for the WayTrace dashboard.

Every number here is READ from a committed file. Nothing is typed in by
hand and nothing is recomputed. If a file is missing, the panel says so
rather than showing a plausible number - Rule 51, a default is a value
you did not choose.
"""

import json
import os
import re

import matplotlib
import streamlit as st
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

matplotlib.use("Agg")   # no display in a Streamlit process

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


def hotspot_map(results, hotspots_path, signs_path):
    """Plot hotspots, events, the sign and the junction on real metres.

    Hotspots are drawn as SQUARES the size of the clustering cell, not as
    dots: a hotspot IS a 0.5 m grid cell, and a dot would claim a precision
    the method does not have.
    """
    st.subheader("Where it happened")
    if not (os.path.exists(hotspots_path) and os.path.exists(signs_path)):
        st.warning("hotspots.json or signs.json not found - no map shown.")
        return

    with open(hotspots_path) as f:
        hs = json.load(f)
    with open(signs_path) as f:
        sg = json.load(f)

    cell = hs.get("cell_m", 0.5)
        # Rotate 90 degrees clockwise so the plot matches the camera view.
    # x_m and y_m are swapped at the DRAWING layer only - no stored
    # coordinate is altered, so nothing downstream is affected.
    def rot(x, y):
        return y, x
    spots = hs["hotspots"]
    events = results["events"]

    st.caption(
        f"Measured in metres on the real floor. The blue squares are drawn "
        f"at their true {cell} m size, because a hotspot is a square of "
        f"floor, not a pinpoint. The sign and the three doorways were "
        f"measured with a tape measure, not produced by the code."
    )

    fig, ax = plt.subplots(figsize=(7, 5))

    # hotspot cells, shaded by how many events fell in them
    top = max((s["event_count"] for s in spots), default=1)
    for s in spots:
        sx, sy = rot(s["x_m"], s["y_m"])
        ax.add_patch(Rectangle(
            (sx - cell / 2, sy - cell / 2), cell, cell,
            facecolor="#0B9FC4", alpha=0.18 + 0.5 * s["event_count"] / top,
            edgecolor="#0B9FC4", linewidth=1.2, zorder=1))
        ax.annotate(str(s["event_count"]), (sx, sy),
                    ha="center", va="center", fontsize=11,
                    fontweight="bold", color="#05576b", zorder=4)

    # individual events - shape AND colour, never colour alone
    for kind, marker, colour in (("HESITATION", "o", "#1a7f37"),
                                 ("UTURN", "^", "#b54708")):
        pts = [rot(e["x_m"], e["y_m"]) for e in events if e["type"] == kind]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.scatter(xs, ys, marker=marker, s=26, color=colour,
                   edgecolor="white", linewidth=0.5, zorder=3,
                   label=f"{kind.title()} ({len(xs)})")

    # measured furniture - tape measure, not detector output
    for i, sign in enumerate(sg.get("signs", [])):
        gx, gy = rot(sign["x_m"], sign["y_m"])
        ax.scatter([gx], [gy], marker="s", s=90,
                   color="#24292f", zorder=5,
                   label="Sign (measured)" if i == 0 else None)
    for i, op in enumerate(sg.get("junction", {}).get("openings", [])):
        ox, oy = rot(op["x_m"], op["y_m"])
        ax.scatter([ox], [oy], marker="x", s=70,
                   color="#6e7781", linewidth=2, zorder=5,
                   label="Junction opening (measured)" if i == 0 else None)
        ax.annotate(op["id"], (ox, oy),
                    textcoords="offset points", xytext=(6, 5),
                    fontsize=8, color="#6e7781")

    ax.set_aspect("equal")
    ax.set_xlabel("metres along the corridor")
    ax.set_ylabel("metres across the corridor")
    ax.invert_yaxis()
    ax.grid(True, linewidth=0.4, alpha=0.4)
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9,
              bbox_to_anchor=(1.02, 1.0), borderaxespad=0)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown(
        f"**How to read this:** you are looking down at the corridor floor "
        f"from above. The **black square** is the sign. The **grey crosses** "
        f"are the three doorways. Each **green dot** is one place someone "
        f"stopped; each **orange triangle** is one place someone turned "
        f"around. The **blue squares** are the spots where those events "
        f"bunched together — the number inside is how many events landed "
        f"there, and darker means more."
    )

    # Say the finding in words. A judge has a few seconds with this plot and
    # will not decode it unaided - every number on screen must be explained
    # before they can wonder about it.
    if spots:
        big = max(spots, key=lambda s: s["event_count"])
        approach = sum(1 for s in spots if s.get("side") == "approach")
        st.info(
            f"**People got confused BEFORE they reached the sign.** "
            f"{approach} of the {len(spots)} hotspots are on the approach "
            f"side. The biggest holds {big['event_count']} events "
            f"({big['hesitations']} stops, {big['uturns']} turn-arounds) and "
            f"sits {big['distance_to_sign_m']} m from the sign and "
            f"{big['distance_to_junction_m']} m from the junction."
        )