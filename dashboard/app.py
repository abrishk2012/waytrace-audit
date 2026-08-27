import json
import os
import streamlit as st

st.set_page_config(page_title="WayTrace", layout="wide")

WEB_DIR = "data/web"
RESULTS = "data/output/results.json"
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("WayTrace")
st.caption("Wayfinding friction detection from ceiling-mounted CCTV")

with open(RESULTS) as f:
    results = json.load(f)

clips = sorted({t["clip"] for t in results["trips_examined"]},
               key=lambda c: int(c.replace("clip", "")))

mode = st.radio("Source", ["Recorded clip", "Upload your own"], horizontal=True)

if mode == "Recorded clip":
    clip = st.selectbox("Clip", clips)
    video_path = os.path.join(WEB_DIR, f"{clip}_traj.mp4")
    if os.path.exists(video_path):
        st.video(video_path)
    else:
        st.error(f"No video found at {video_path}")

else:
    up = st.file_uploader("Corridor footage (mp4)", type=["mp4"])
    if up is not None:
        dest = os.path.join(UPLOAD_DIR, up.name)
        with open(dest, "wb") as f:
            f.write(up.getbuffer())
        size_mb = round(os.path.getsize(dest) / 1024 / 1024, 1)
        st.success(f"Saved {up.name} ({size_mb} MB)")
        st.video(dest)