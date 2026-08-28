"""Pipeline progress UI for the WayTrace dashboard.

Rendering only. Nothing here starts, waits on, or inspects the pipeline -
it is handed a state and draws it. Add or reorder stages by editing
STAGES; the drawing code never needs to change.
"""

import streamlit as st

STAGES = [
    {"key": "convert", "name": "Convert",
     "desc": "Re-encodes the upload to a constant 15 frames per second, so a "
             "frame number maps to a real second"},
    {"key": "undistort", "name": "Undistort",
     "desc": "Corrects the lens barrel distortion in the video frames, using "
             "the EZVIZ calibration"},
    {"key": "track", "name": "Track",
     "desc": "Finds each person and follows them frame to frame. The slow "
             "stage: about 0.55 s per frame on CPU"},
    {"key": "detect", "name": "Detect",
     "desc": "Applies the eight locked thresholds to the trajectories to find "
             "hesitations and U-turns"},
    {"key": "encode", "name": "Encode",
     "desc": "Re-encodes the tracked video to H.264 so a browser can play it"},
]

_GLYPH = {"done": "&#10003;", "running": "&#9679;",
          "upcoming": "", "failed": "&#10005;"}
_WORD = {"done": "done", "running": "running",
         "upcoming": "not started", "failed": "failed"}

_CSS = """<style>
/* No background colour is used anywhere. Two earlier attempts failed:
   prefers-color-scheme reads the OS, not Streamlit, and Streamlit does not
   publish --background-color here. Upcoming nodes are TRANSPARENT with a
   thicker ring, so they are correct in every theme by construction. */
.wt-pipe{--wt-on:#0B9FC4;--wt-off:rgba(11,159,196,.35);--wt-fail:#D93025;
--wt-muted:#8a8f98;position:relative;display:flex;width:100%;
margin:2.6rem 0 1.2rem;font-size:.8rem;}

.wt-seg{position:absolute;top:16px;height:6px;border-radius:3px;
background:var(--wt-off);}
.wt-seg.on{background:var(--wt-on);}

.wt-step{flex:1 1 0;min-width:0;position:relative;display:flex;
flex-direction:column;align-items:center;outline:none;cursor:default;}
.wt-nodewrap{height:38px;display:flex;align-items:center;
justify-content:center;position:relative;z-index:1;}

/* One variable sets both axes. min/max on both stops flex, the glyph or
   line-height from stretching it - the Day 17 oval bug, measured at
   22.667 x 18.667 in devtools before this was fixed. */
.wt-node{--d:30px;border-radius:50%;display:grid;place-items:center;
line-height:0;color:#fff;font-weight:700;box-sizing:border-box;
flex:0 0 auto;padding:0;width:var(--d);height:var(--d);
min-width:var(--d);max-width:var(--d);
min-height:var(--d);max-height:var(--d);}

.wt-label{margin-top:.15rem;max-width:100%;overflow:hidden;
text-overflow:ellipsis;white-space:nowrap;color:var(--wt-muted);}

/* upcoming: smaller, hollow ring, no fill */
.wt-step.upcoming .wt-node{--d:20px;background:transparent;
border:4px solid var(--wt-off);}
/* done: filled, white tick */
.wt-step.done .wt-node{--d:30px;background:var(--wt-on);
border:3px solid var(--wt-on);font-size:.95rem;}
.wt-step.done .wt-label{color:var(--wt-on);}
/* running: same size as done, marked out by the pulse alone */
.wt-step.running .wt-node{--d:30px;background:var(--wt-on);
border:3px solid var(--wt-on);font-size:.7rem;
animation:wt-pulse 1.6s ease-out infinite;}
.wt-step.running .wt-label{color:var(--wt-on);font-weight:600;}
/* failed: red circle, white cross */
.wt-step.failed .wt-node{--d:34px;background:var(--wt-fail);
border:3px solid var(--wt-fail);font-size:1rem;}
.wt-step.failed .wt-label{color:var(--wt-fail);font-weight:600;}

@keyframes wt-pulse{0%{box-shadow:0 0 0 0 rgba(11,159,196,.5);}
70%{box-shadow:0 0 0 10px rgba(11,159,196,0);}
100%{box-shadow:0 0 0 0 rgba(11,159,196,0);}}
@media (prefers-reduced-motion:reduce){.wt-step.running .wt-node
{animation:none;box-shadow:0 0 0 4px rgba(11,159,196,.35);}}
.wt-step:focus .wt-node{box-shadow:0 0 0 4px rgba(11,159,196,.6);}

.wt-tip{position:absolute;bottom:calc(100% + 10px);left:50%;
transform:translateX(-50%);width:max-content;max-width:215px;
background:#24292f;color:#fff;padding:.4rem .55rem;border-radius:6px;
font-size:.72rem;line-height:1.3;text-align:left;opacity:0;
visibility:hidden;transition:opacity .12s;z-index:5;pointer-events:none;}
.wt-step:hover .wt-tip,.wt-step:focus .wt-tip,
.wt-step:focus-within .wt-tip{opacity:1;visibility:visible;}
.wt-step:first-child .wt-tip{left:0;transform:none;}
.wt-step:last-child .wt-tip{left:auto;right:0;transform:none;}

@media (max-width:560px){.wt-pipe{font-size:.68rem;}
.wt-nodewrap{height:30px;}.wt-seg{top:12px;height:5px;}
.wt-step.upcoming .wt-node{--d:16px;border-width:3px;}
.wt-step.done .wt-node{--d:24px;font-size:.8rem;}
.wt-step.running .wt-node{--d:24px;}
.wt-step.failed .wt-node{--d:26px;font-size:.85rem;}}
</style>"""


def stage_states(done_upto, running=None, failed=None):
    """Turn (done_upto, running, failed) into one status per stage."""
    out = []
    for i in range(len(STAGES)):
        if failed is not None and i == failed:
            out.append("failed")
        elif i < done_upto:
            out.append("done")
        elif running is not None and i == running:
            out.append("running")
        else:
            out.append("upcoming")
    return out


def _html(states):
    n = len(STAGES)
    half = 50.0 / n                      # first/last node centres, in percent
    span = 100.0 - 2 * half              # rail length between those centres
    started = [i for i, s in enumerate(states) if s != "upcoming"]
    active = max(started) if started else 0
    frac = 1.0 if n < 2 else active / (n - 1)
    if all(s == "done" for s in states):
        frac = 1.0

    parts = [_CSS,
             '<div class="wt-pipe" role="list" aria-label="Pipeline progress">']
    # One segment per gap, stopping 22px short of each node centre so the
    # line never crosses a hollow circle. Rule 43: the single-bar version
    # was measured showing through, not assumed to.
    for i in range(n - 1):
        left = half + i * (span / (n - 1))
        on = "on" if states[i] != "upcoming" and states[i + 1] != "upcoming" \
             or (states[i] != "upcoming" and i + 1 <= active) else ""
        parts.append(
            f'<div class="wt-seg {on}" style="left:calc({left:.2f}% + 22px);'
            f'width:calc({span / (n - 1):.2f}% - 44px);"></div>')
    for stage, state in zip(STAGES, states):
        label = f"{stage['name']}: {_WORD[state]}. {stage['desc']}."
        parts.append(
            f'<div class="wt-step {state}" role="listitem" tabindex="0" '
            f'aria-label="{label}">'
            f'<div class="wt-nodewrap">'
            f'<div class="wt-node" aria-hidden="true">{_GLYPH[state]}</div>'
            f'</div>'
            f'<div class="wt-label">{stage["name"]}</div>'
            f'<div class="wt-tip" aria-hidden="true">'
            f'<b>{stage["name"]}</b> &ndash; {_WORD[state]}<br>'
            f'{stage["desc"]}</div>'
            f'</div>')
    parts.append('</div>')
    return "".join(parts)


def draw_stages(slot, done_upto, running=None, failed=None):
    """Draw the pipeline into a slot. Drop-in for the old draw_stages."""
    slot.markdown(_html(stage_states(done_upto, running, failed)),
                  unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(page_title="Pipeline UI preview", layout="wide")
    st.title("Pipeline UI preview")
    st.caption("Rendering only. No video is read and nothing is written.")
    for caption, args in [
        ("Nothing started yet", (0, 0)),
        ("Two done, tracking now", (2, 2)),
        ("Detect failed", (3, None, 3)),
        ("All five done", (5,)),
    ]:
        st.subheader(caption)
        draw_stages(st.empty(), *args)