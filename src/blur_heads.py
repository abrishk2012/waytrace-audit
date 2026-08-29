"""
blur_heads.py - pixelate the head region of every tracked person.

Reads box positions from data/output/*_traj.json (columns:
foot_x, foot_y, frame_number, box_w, box_h - all PIXELS in the
undistorted frame). Writes a blurred copy of data/web/<clip>_traj.mp4.

Two modes:
  --check   draw solid yellow rectangles on ONE frame, save a PNG.
            Use this FIRST to confirm the rectangles sit on the heads.
  --run     process the whole clip and write the output video.

Why not a face detector: the box is already saved, and a ceiling camera
often shows the top of a head rather than a face. Running fresh inference
would cost hours and detect less.
"""

import cv2
import numpy as np
import json
import glob
import sys
import os

# ---------------------------------------------------------------- settings

HEAD_FRACTION = 0.30   # top 30% of the person box is the head region
MARGIN_X = 0.0
HEAD_WIDTH = 1.0       # widen sideways by 15% of box width each side
MARGIN_Y = 0.10        # extend downwards by 10% of box height
MOSAIC_PX = 6          # head region is squashed to this many pixels wide
MAX_INTERP_GAP = 8     # holes up to this length are interpolated
FRAME_OFFSET = 1       # JSON frame_number 1 == video frame index 0

CHECK_COLOUR = (0, 212, 255)  # BGR - signage yellow


# ---------------------------------------------------------------- geometry

def box_from_point(point):
    """Turn one JSON row into a pixel rectangle (x1, y1, x2, y2)."""
    foot_x, foot_y, _frame, box_w, box_h = point
    x1 = foot_x - box_w // 2
    x2 = foot_x + box_w // 2
    y1 = foot_y - box_h
    y2 = foot_y
    return x1, y1, x2, y2


def head_rect(box):
    """
    Top slice of the person box, guarded against raised arms.

    Measured from your own data: the median box is 2.41x taller than
    wide, 95% are under 3.38. Anything past 3.0 has an arm in it, so
    the height is capped there. Width is capped too, because a raised
    arm also pushes one side of the box out and drags the centre with it.
    """
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    cx = (x1 + x2) // 2

    # cap height: past 3.0x width, the extra is arm, not head
    max_h = int(w * 3.0)
    if h > max_h:
        h = max_h
        y1 = y2 - h

    # cap width: a normal body is about h/2.41 wide
    body_w = min(w, int(h / 2.41))
    hw = int(body_w * HEAD_WIDTH / 2)

    return (cx - hw,
            y1 + 2,
            cx + hw,
            y1 + int(h * HEAD_FRACTION))

def union(a, b):
    """Smallest rectangle containing both."""
    return (min(a[0], b[0]), min(a[1], b[1]),
            max(a[2], b[2]), max(a[3], b[3]))


def lerp(a, b, t):
    return a + (b - a) * t


# ------------------------------------------------------------ build the map

def build_frame_map(traj_path):
    """
    frame index (0-based, video) -> list of head rectangles.

    Holes inside a track's lifetime are filled. Short holes are
    interpolated. Long holes get the union of both endpoints, because
    guessing a path across 24 frames is not something we can verify.
    """
    data = json.load(open(traj_path))
    frames = {}
    filled_short = 0
    filled_long = 0

    def add(frame_number, rect):
        idx = frame_number - FRAME_OFFSET
        if idx < 0:
            return
        frames.setdefault(idx, []).append(rect)

    for track in data.values():
        points = sorted(track, key=lambda p: p[2])
        by_frame = {p[2]: p for p in points}

        for p in points:
            add(p[2], head_rect(box_from_point(p)))

        # walk consecutive detections and fill anything between them
        for i in range(len(points) - 1):
            f_a = points[i][2]
            f_b = points[i + 1][2]
            gap = f_b - f_a - 1
            if gap <= 0:
                continue

            box_a = box_from_point(by_frame[f_a])
            box_b = box_from_point(by_frame[f_b])

            if gap <= MAX_INTERP_GAP:
                for f in range(f_a + 1, f_b):
                    t = (f - f_a) / (f_b - f_a)
                    mid = tuple(int(lerp(box_a[k], box_b[k], t))
                                for k in range(4))
                    add(f, head_rect(mid))
                    filled_short += 1
            else:
                safe = union(head_rect(box_a), head_rect(box_b))
                for f in range(f_a + 1, f_b):
                    add(f, safe)
                    filled_long += 1

    return frames, filled_short, filled_long


def verify(traj_path, frames):
    """
    The proof. Count frames inside any track's lifetime that have no
    rectangle. If this is 0, every frame containing a tracked person
    is covered.
    """
    data = json.load(open(traj_path))
    uncovered = []
    for tid, track in data.items():
        fr = sorted(p[2] for p in track)
        for f in range(fr[0], fr[-1] + 1):
            if (f - FRAME_OFFSET) not in frames:
                uncovered.append((tid, f))
    return uncovered


# ---------------------------------------------------------------- pixelate

def pixelate(frame, rect):
    h, w = frame.shape[:2]
    x1 = max(0, rect[0]); y1 = max(0, rect[1])
    x2 = min(w, rect[2]); y2 = min(h, rect[3])
    if x2 - x1 < 2 or y2 - y1 < 2:
        return
    patch = frame[y1:y2, x1:x2]
    small_h = max(2, int(MOSAIC_PX * (y2 - y1) / max(1, x2 - x1)))
    small = cv2.resize(patch, (MOSAIC_PX, small_h),
                       interpolation=cv2.INTER_AREA)
    soft = cv2.resize(small, (x2 - x1, y2 - y1),
                      interpolation=cv2.INTER_LINEAR)
    k = max(3, ((x2 - x1) // 6) * 2 + 1)
    soft = cv2.GaussianBlur(soft, (k, k), 0)

    # fade: 1 in the middle, 0 at the edges, so there is no hard line
    mask = np.zeros((y2 - y1, x2 - x1), np.float32)
    cv2.ellipse(mask,
                ((x2 - x1) // 2, (y2 - y1) // 2),
                ((x2 - x1) // 2, (y2 - y1) // 2),
                0, 0, 360, 1.0, -1)
    fk = max(3, ((x2 - x1) // 4) * 2 + 1)
    mask = cv2.GaussianBlur(mask, (fk, fk), 0)[:, :, None]

    frame[y1:y2, x1:x2] = (soft * mask + patch * (1 - mask)).astype("uint8")


# -------------------------------------------------------------------- main

def find_traj(clip):
    hits = glob.glob(f"data/output/*{clip}_traj.json")
    if len(hits) != 1:
        raise SystemExit(f"expected 1 traj file for {clip}, found {len(hits)}")
    return hits[0]


def main():
    if len(sys.argv) < 3:
        raise SystemExit("usage: python src/blur_heads.py clip10 --check [frame]\n"
                         "       python src/blur_heads.py clip10 --run")

    clip = sys.argv[1]
    mode = sys.argv[2]

    traj_path = find_traj(clip)
    video_in = f"data/web/{clip}_traj.mp4"
    if not os.path.exists(video_in):
        raise SystemExit(f"missing {video_in}")

    frames, short, long = build_frame_map(traj_path)
    uncovered = verify(traj_path, frames)

    print(f"traj:        {traj_path}")
    print(f"video:       {video_in}")
    print(f"frames with a rectangle: {len(frames)}")
    print(f"holes filled by interpolation (<={MAX_INTERP_GAP}): {short}")
    print(f"holes filled by union (>{MAX_INTERP_GAP}):          {long}")
    print(f"UNCOVERED FRAMES INSIDE A TRACK: {len(uncovered)}")
    if uncovered:
        print("  first few:", uncovered[:10])

    cap = cv2.VideoCapture(video_in)
    if not cap.isOpened():
        raise SystemExit(f"could not open {video_in}")

    if mode == "--check":
        target = int(sys.argv[3]) if len(sys.argv) > 3 else None
        if target is None:
            target = sorted(frames)[len(frames) // 2]
        cap.set(cv2.CAP_PROP_POS_FRAMES, target)
        ok, frame = cap.read()
        cap.release()
        if not ok:
            raise SystemExit(f"could not read frame {target}")
        for r in frames.get(target, []):
            cv2.rectangle(frame, (r[0], r[1]), (r[2], r[3]), CHECK_COLOUR, 2)
        out = f"data/output/_blurcheck_{clip}_f{target}.png"
        cv2.imwrite(out, frame)
        print(f"\nCHECK frame {target}, {len(frames.get(target, []))} rectangle(s)")
        print(f"wrote {out} - OPEN IT. The boxes must sit on the heads.")
        return

    if mode != "--run":
        raise SystemExit("mode must be --check or --run")

    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out_path = f"data/web/{clip}_traj_blur.mp4"
    writer = cv2.VideoWriter(out_path,
                             cv2.VideoWriter_fourcc(*"mp4v"),
                             fps, (w, h))

    idx = 0
    blurred = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        rects = frames.get(idx, [])
        for r in rects:
            pixelate(frame, r)
        if rects:
            blurred += 1
        writer.write(frame)
        idx += 1

    cap.release()
    writer.release()
    print(f"\nwrote {out_path}")
    print(f"frames read: {idx}, frames with a blur applied: {blurred}")
    print("NOTE: mp4v codec. Re-encode to h264 with ffmpeg before the dashboard uses it.")


if __name__ == "__main__":
    main()
