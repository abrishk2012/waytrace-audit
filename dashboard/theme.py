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

PANEL = "#11151A"       # sign face
RAISED = "#1A1F26"      # metric tiles
EDGE = "#2A313A"        # hairline rules
INK = "#F2F4F6"         # primary type
DIM = "#8C949E"         # secondary type
YELLOW = "#FFD400"      # the finding, and nothing else

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&display=swap');

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

/* Section headings, set tight and heavy like a sign. */
h2, h3 {{
    font-weight: 700 !important;
    letter-spacing: -0.01em;
}}

/* Soften the callout boxes to match the tiles. */
[data-testid="stAlert"] {{
    border-radius: 10px;
}}
</style>
"""


def inject():
    """Apply the theme. Call once, immediately after set_page_config."""
    st.markdown(_CSS, unsafe_allow_html=True)
