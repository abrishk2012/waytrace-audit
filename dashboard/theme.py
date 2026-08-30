"""Visual theme for the WayTrace dashboard.

The dashboard is styled as airport wayfinding signage, because signage is
what this system audits. Dark charcoal panels, one typeface at strict
weights, and a single yellow reserved for the finding itself.

That is not decoration. Signage exists to be read quickly, at distance, by
people who are not concentrating - which is also the problem a judge
watching a two-minute video has. High contrast additionally survives video
compression, which pale colours on white do not.

Colours here MUST match .streamlit/config.toml and the matplotlib rcParams
in panels.py. Three places, one palette.
"""

import streamlit as st
import base64
from pathlib import Path

_FONT_FILE = Path(__file__).parent / "fonts" / "Archivo.woff2"
_ARCHIVO_B64 = base64.b64encode(_FONT_FILE.read_bytes()).decode("ascii")

PANEL = "#11151A"       # sign face
WASH = "#1B2129"        # gradient high point, 9 points of luminance above PANEL
RAISED = "#1A1F26"      # metric tiles
EDGE = "#2A313A"        # hairline rules
INK = "#F2F4F6"         # primary type
DIM = "#8C949E"         # secondary type
YELLOW = "#FFD400"      # the finding, and nothing else

_CSS = f"""
<style>
@font-face {{
    font-family: 'Archivo';
    font-style: normal;
    font-weight: 400 700;
    font-display: swap;
    src: url('data:font/woff2;base64,{_ARCHIVO_B64}') format('woff2');
}}

/* Streamlit caps the content width even at layout="wide". Release it -
   a judge watching a compressed video needs the plots as large as the
   frame allows. */
.block-container,
[data-testid="stMainBlockContainer"] {{
    max-width: 100% !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    padding-top: 2rem !important;
}}

/* A very shallow wash from the top-left, the way light falls across a
   sign face rather than lying flat on it. Deliberately subtle: video
   compression turns any strong gradient into visible banding, and the
   two stops here are 9 points apart in luminance. */
[data-testid="stAppViewContainer"] {{
    background:
        radial-gradient(1100px 720px at 12% -12%, {WASH} 0%, {PANEL} 58%),
        {PANEL};
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

/* Section headings carry the yellow rule from docs/architecture.svg -
   a bar beside the title, the way a destination band sits beside the
   text on an overhead sign. Same device, so the diagram and the
   dashboard read as one system. */
h2, h3 {{
    font-weight: 700 !important;
    letter-spacing: -0.01em;
    position: relative;
    padding-left: 20px !important;
}}

h2::before, h3::before {{
    content: "";
    position: absolute;
    left: 0;
    top: 0.18em;
    bottom: 0.18em;
    width: 5px;
    border-radius: 2px;
    background: {YELLOW};
}}

/* Metric tiles read as sign panels: soft corners, a hairline edge, and a
   yellow rule along the top edge the way a destination band sits above the
   text on an overhead sign. */
[data-testid="stMetric"] {{
    background: {RAISED};
    border: 1px solid {EDGE};
    border-top: 3px solid {YELLOW};
    border-radius: 10px;
    padding: 14px 18px 16px 18px;
}}

[data-testid="stMetricLabel"] p {{
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: {DIM} !important;
}}

[data-testid="stMetricValue"] {{
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.02em;
    color: {INK};
}}

/* Callout boxes: the same soft-cornered treatment as the tiles, with more
   room inside and a looser line. These are read on a compressed video, at
   a distance, by someone not concentrating.
   NO colour is set here on purpose. Streamlit tints info, warning and
   error differently, and the red on the U-turn-zero box is a signal - the
   one panel that says the detector failed should not look like the rest. */
[data-testid="stAlert"] {{
    border-radius: 10px;
    padding: 0;
}}

/* The inset lives on the INNER container, measured in devtools as the one
   that was clipping its own content. One box owns the padding; the outer
   one owns the corner and the colour. */
[data-testid="stAlertContainer"] {{
    height: auto !important;
    align-items: flex-start !important;
    padding: 20px 22px !important;
}}

[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {{
    max-width: none;
}}

[data-testid="stAlert"] p {{
    line-height: 1.65;
    margin-bottom: 0.6rem;
}}

[data-testid="stAlert"] [data-testid="stMarkdownContainer"] > *:first-child {{
    margin-top: 0 !important;
}}

[data-testid="stAlert"] [data-testid="stMarkdownContainer"] > *:last-child {{
    margin-bottom: 0 !important;
}}

/* Bordered containers, matched to the metric tiles. */
[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {RAISED};
    border: 1px solid {EDGE};
    border-radius: 12px;
    padding: 18px 20px !important;
}}

/* A hairline between columns that share one box. Drawn on the left edge
   of every column except the first, so it appears between them and not
   at the outer edges. Only inside a bordered container - plain columns
   elsewhere on the page keep no rule. */
[data-testid="stVerticalBlockBorderWrapper"]
[data-testid="stColumn"]:not(:first-child) {{
    border-left: 1px solid {EDGE};
    padding-left: 26px;
}}

/* Space between a section heading and whatever it introduces. */
h2, h3 {{
    margin-bottom: 0.85rem !important;
}}

/* ---- Scroll reveal ---------------------------------------------------
   Streamlit strips <script>, so there is no IntersectionObserver here.
   This is CSS scroll-driven animation instead - the browser ties the
   animation to the element's position in the viewport with no JS at all.

   Wrapped in @supports on purpose. Where it is not supported the rules
   never apply, so nothing starts at opacity 0 and nothing can end up
   permanently invisible. A decoration must not be able to hide content. */
@supports (animation-timeline: view()) {{
    @media (prefers-reduced-motion: no-preference) {{
        [data-testid="stMetric"],
        [data-testid="stVerticalBlockBorderWrapper"],
        .wt-claim,
        [data-testid="stAlert"] {{
            animation: wt-reveal linear both;
            animation-timeline: view();
            animation-range: entry 5% cover 22%;
        }}
    }}
}}

@keyframes wt-reveal {{
    from {{ opacity: 0; transform: translateY(14px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

/* ---- Claim block -----------------------------------------------------
   A finding. The heading is set at 60% of the section-heading size, with
   a thin yellow rule - the same device as the h2, one step quieter, so
   the hierarchy reads as section > claim > detail.
   The heading and the lead line are always visible. Only the supporting
   detail is behind the hover. */
.wt-claim {{
    position: relative;
    display: block;
    padding: 14px 18px 15px 18px;
    margin: 0 0 12px 0;
    background: {RAISED};
    border: 1px solid {EDGE};
    border-left: 2px solid {YELLOW};
    border-radius: 8px;
    outline: none;
    transition: border-color 150ms ease, background 150ms ease;
}}

.wt-claim:hover,
.wt-claim:focus-visible {{
    border-color: {EDGE};
    border-left-color: {YELLOW};
    background: #1E242C;
}}

.wt-claim-head {{
    display: block;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: {INK};
    margin-bottom: 6px;
}}

.wt-claim-lead {{
    display: block;
    font-size: 0.92rem;
    line-height: 1.55;
    color: {INK};
}}

.wt-claim-more {{
    display: grid;
    grid-template-rows: 0fr;
    opacity: 0;
    transition: grid-template-rows 200ms ease, opacity 160ms ease,
                margin-top 200ms ease;
    margin-top: 0;
}}

.wt-claim:hover .wt-claim-more,
.wt-claim:focus-visible .wt-claim-more {{
    grid-template-rows: 1fr;
    opacity: 1;
    margin-top: 10px;
}}

.wt-claim-more > * {{
    overflow: hidden;
    min-height: 0;
}}

.wt-claim-more p {{
    font-size: 0.86rem;
    line-height: 1.55;
    color: {DIM};
    margin: 0 0 6px 0;
    max-width: none;
}}

.wt-claim-more p:last-child {{
    margin-bottom: 0;
}}

@media (prefers-reduced-motion: reduce) {{
    .wt-claim, .wt-claim-more {{ transition: none; }}
}}

/* ---- Hover explanation ----------------------------------------------
   A "How to read this?" trigger for LEGENDS ONLY. Anything in here is
   invisible in a screen recording, so no measured result is ever put
   behind it. Opens on hover and on keyboard focus, so it is reachable
   without a mouse. */
.wt-help {{
    position: relative;
    display: inline-block;
    outline: none;
    z-index: 30;
}}

.wt-help-trigger {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    color: {DIM};
    border: 1px solid {EDGE};
    border-radius: 999px;
    padding: 5px 12px 5px 10px;
    cursor: help;
    transition: color 140ms ease, border-color 140ms ease;
}}

.wt-help:hover .wt-help-trigger,
.wt-help:focus-visible .wt-help-trigger {{
    color: {YELLOW};
    border-color: {YELLOW};
}}

.wt-help-panel {{
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    width: 420px;
    max-width: 78vw;
    background: {RAISED};
    border: 1px solid {EDGE};
    border-left: 3px solid {YELLOW};
    border-radius: 10px;
    padding: 16px 18px;
    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.55);
    opacity: 0;
    visibility: hidden;
    transform: translateY(-4px);
    transition: opacity 130ms ease, transform 130ms ease,
                visibility 0s linear 130ms;
    z-index: 40;
}}

.wt-help:hover .wt-help-panel,
.wt-help:focus-visible .wt-help-panel {{
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
    transition: opacity 130ms ease, transform 130ms ease,
                visibility 0s linear 0s;
}}

.wt-help-panel strong {{
    display: block;
    font-size: 0.9rem;
    color: {INK};
    margin-bottom: 8px;
}}

.wt-help-panel p {{
    font-size: 0.85rem;
    line-height: 1.55;
    color: {DIM};
    margin: 0 0 7px 0;
    max-width: none;
}}

.wt-help-panel p:last-child {{
    margin-bottom: 0;
}}

.wt-help-panel b {{
    color: {INK};
}}

/* A floating panel is clipped by any ancestor that hides its overflow.
   Streamlit wraps every element in several. */
[data-testid="stVerticalBlock"],
[data-testid="stElementContainer"] {{
    overflow: visible !important;
}}

@media (prefers-reduced-motion: reduce) {{
    .wt-help-panel {{ transition: none; }}
}}

/* Captions sit under a figure and explain it. Give them room to breathe
   and stop them running the full width of a wide screen, where a line
   becomes too long to track back from. */
[data-testid="stCaptionContainer"] p {{
    line-height: 1.6;
    max-width: 110ch;
}}

/* Body prose, same reason. */
[data-testid="stMarkdownContainer"] p {{
    line-height: 1.65;
    max-width: 110ch;
}}
</style>
"""


def inject():
    """Apply the theme. Call once, immediately after set_page_config."""
    st.markdown(_CSS, unsafe_allow_html=True)
