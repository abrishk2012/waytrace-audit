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
    padding: 18px 22px 24px 22px;
}}

/* No width cap inside an alert. The alert's own container decides the
   width - when two sit side by side in columns, that is half the page. */
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {{
    max-width: none;
}}

[data-testid="stAlert"] p {{
    line-height: 1.65;
    margin-bottom: 0.55rem;
}}

[data-testid="stAlert"] p:last-child {{
    margin-bottom: 0;
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
