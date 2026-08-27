import json
import os
import streamlit as st

st.set_page_config(page_title="WayTrace", layout="wide")

WEB_DIR = "data/web"
RESULTS = "data/output/results.json"

st.title("WayTrace")
st.caption("Wayfinding friction detection from ceiling-mounted CCTV")

with open(RESULTS) as f:
    results = json.load(f)

clips = sorted({t["clip"] for t in results["trips_examined"]},
               key=lambda c: int(c.replace("clip", "")))

clip = st.selectbox("Clip", clips)

video_path = os.path.join(WEB_DIR, f"{clip}_traj.mp4")

if os.path.exists(video_path):
    st.video(video_path)
else:
    st.error(f"No video found at {video_path}")