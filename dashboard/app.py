import json
import os
import shutil
import subprocess
import sys
import cv2
import streamlit as st
from panels import counts_panel, accuracy_panel, parse_per_behaviour, hotspot_map, timeline_panel


st.set_page_config(page_title="WayTrace", layout="wide")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(ROOT, "data", "web")
RESULTS = os.path.join(ROOT, "data", "output", "results.json")
UPLOAD_DIR = os.path.join(ROOT, "data", "uploads")
SCRATCH = os.path.join(ROOT, "data", "scratch")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SCRATCH, exist_ok=True)

st.title("WayTrace")
st.caption("Wayfinding friction detection from ceiling-mounted CCTV")

with open(RESULTS) as f:
    results = json.load(f)

clips = sorted({t["clip"] for t in results["trips_examined"]},
               key=lambda c: int(c.replace("clip", "")))
PER_BEHAVIOUR = os.path.join(ROOT, "data", "per_behaviour_day15.txt")
per_behaviour = parse_per_behaviour(PER_BEHAVIOUR)


def run_stage(cmd, label, total_frames, slot, done_upto, running, status):
    """Run a pipeline script, creeping the rail from its 'Frame N' prints.

    The rail IS the progress bar. A separate st.progress bar used to sit
    below it showing the same thing, which read as two bars disagreeing.
    """
    status.write(label)
    draw_stages(slot, done_upto, running, frac=0.0)
    if cmd and cmd[0] == sys.executable:
        cmd = [cmd[0], "-u"] + list(cmd[1:])   # unbuffered: Frame N arrives live
    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, bufsize=1)
    tail = []
    for line in proc.stdout:
        tail.append(line.rstrip())
        tail = tail[-5:]
        if line.startswith("Frame ") or line.startswith("  frame"):
            try:
                n = int(line.split()[-1])
                draw_stages(slot, done_upto, running,
                            frac=min(n / total_frames, 1.0))
            except ValueError:
                pass
    proc.wait()
    return proc.returncode, tail

counts_panel(results)
accuracy_panel(per_behaviour)
hotspot_map(results,
            os.path.join(ROOT, "data", "output", "hotspots.json"),
            os.path.join(ROOT, "data", "signs.json"))
timeline_panel(results, os.path.join(ROOT, "data", "trip.csv"))
st.divider()
mode = st.radio("Source", ["Recorded clip", "Upload your own"], horizontal=True)

if mode == "Recorded clip":
    clip = st.selectbox("Clip", clips)
    video_path = os.path.join(WEB_DIR, f"{clip}_traj.mp4")
    if os.path.exists(video_path):
        st.video(video_path)
    else:
        st.error(f"No video found at {video_path}")

else:
    st.info(
        "Upload footage **from this camera only**. The homography maps this "
        "camera's pixels to metres on this corridor floor. Footage from a "
        "different camera or position would produce real detections at "
        "meaningless coordinates. Recalibration is a ~20 minute deployment step."
    )
    up = st.file_uploader("Corridor footage (mp4)", type=["mp4"])

    if up is not None:
        dest = os.path.join(UPLOAD_DIR, up.name)
        with open(dest, "wb") as f:
            f.write(up.getbuffer())

        cap = cv2.VideoCapture(dest)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        mins = round(frames * 0.549 / 60, 1)

        st.write(f"**{up.name}** - {frames} frames")
        st.warning(
            f"Full analysis runs at about 8x video length on CPU. "
            f"This clip will take roughly **{mins} minutes**."
        )

        if st.button("Analyse", type="primary"):
            stem = "upload"
            und = os.path.join(SCRATCH, f"{stem}.mp4")
            traj = os.path.join(SCRATCH, f"{stem}_traj.json")
            out = os.path.join(SCRATCH, f"{stem}_events.json")
            raw_mp4 = os.path.join(SCRATCH, f"{stem}_traj_raw.mp4")
            web_mp4 = os.path.join(SCRATCH, f"{stem}_traj_web.mp4")
            cfr = os.path.join(SCRATCH, f"{stem}_cfr.mp4")

            steps = st.empty()
            status = st.empty()

            # --- Convert ---
            draw_stages(steps, 0, 0)
            status.write("Converting to constant frame rate...")
            cfr_proc = subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", dest,
                 "-vf", "scale=1024:576", "-r", "15", "-an",
                 "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", cfr],
                cwd=ROOT, capture_output=True, text=True)
            if cfr_proc.returncode != 0:
                draw_stages(steps, 0, failed=0)
                st.error("CFR conversion failed")
                st.code(cfr_proc.stderr[-800:])
                st.stop()

            # --- Undistort ---
            rc, tail = run_stage(
                [sys.executable, "src/undistort_video.py", cfr, und],
                "Undistorting (lens correction)...", frames,
                steps, 1, 1, status)
            if rc != 0:
                draw_stages(steps, 1, failed=1)
                st.error("Undistort failed")
                st.code("\n".join(tail))
                st.stop()

            # --- Track ---
            rc, tail = run_stage(
                [sys.executable, "src/trajectories.py", und],
                "Tracking people (this is the slow part)...", frames,
                steps, 2, 2, status)
            if rc != 0:
                draw_stages(steps, 2, failed=2)
                st.error("Tracking failed")
                st.code("\n".join(tail))
                st.stop()

            for ext, target in ((".json", traj), (".mp4", raw_mp4)):
                produced = os.path.join(ROOT, "data", "output",
                                        f"{stem}_traj{ext}")
                if os.path.exists(produced):
                    shutil.move(produced, target)

            # --- Detect ---
            rc, tail = run_stage(
                [sys.executable, "src/analyse_one.py", traj, out],
                "Running detectors...", frames, steps, 3, 3, status)
            if rc != 0:
                draw_stages(steps, 3, failed=3)
                st.error("Detection failed")
                st.code("\n".join(tail))
                st.stop()

            # --- Encode ---
            draw_stages(steps, 4, 4)
            status.write("Re-encoding for browser playback...")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                            "-i", raw_mp4, "-c:v", "libx264",
                            "-pix_fmt", "yuv420p", "-an", web_mp4],
                           cwd=ROOT, capture_output=True)

            draw_stages(steps, 5)
            status.write("Done.")

            with open(out) as f:
                res = json.load(f)

            st.success(f"{res['tracks_examined']} tracks, "
                       f"{len(res['events'])} events")
            if os.path.exists(web_mp4):
                st.video(web_mp4)
            else:
                st.warning("Tracked video could not be re-encoded for playback.")

            if res["events"]:
                st.dataframe(res["events"], width="stretch")
            else:
                st.write("No hesitations or U-turns detected.")

            st.caption(
                "Precision and recall are not shown here. They are measured "
                "against hand-made labels, and this footage has none. The "
                "62% / 56% held-out figures come from the 25 labelled trips."
            )