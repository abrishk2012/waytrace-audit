import cv2
import json
from collections import defaultdict
from ultralytics import YOLO

video_path = "data/raw/2026-08-19_flat_camC_devwalk_undist.mp4"
output_path = "data/output/devwalk_trajectories.mp4"

MAX_FRAMES = 100000
TRAIL_LENGTH = 60

model = YOLO("yolo11m.pt")

cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
MIN_TRACK_LENGTH = int(fps * 1.0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"),
                         fps, (width, height))

trajectories = defaultdict(list)


def colour_for_id(track_id):
    return ((track_id * 67) % 255,
            (track_id * 131) % 255,
            (track_id * 197) % 255)


frame_number = 0

while frame_number < MAX_FRAMES:
    success, frame = cap.read()
    if not success:
        break
    frame_number += 1

    results = model.track(frame, persist=True, tracker="bytetrack.yaml",
                          imgsz=640, conf=0.25, classes=[0], verbose=False)

    boxes = results[0].boxes

    if boxes.id is not None:
        for box, track_id in zip(boxes.xyxy, boxes.id.int().tolist()):
            x1, y1, x2, y2 = [int(v) for v in box]

            foot_x = (x1 + x2) // 2
            foot_y = y2
            trajectories[track_id].append((foot_x, foot_y, frame_number))

            colour = colour_for_id(track_id)
            cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 1)
            cv2.putText(frame, f"#{track_id}", (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 2)

    for track_id, points in trajectories.items():
        last_seen_frame = points[-1][2]
        if frame_number - last_seen_frame > 5:
            continue

        recent = points[-TRAIL_LENGTH:]
        colour = colour_for_id(track_id)
        for i in range(1, len(recent)):
            p1 = (recent[i - 1][0], recent[i - 1][1])
            p2 = (recent[i][0], recent[i][1])
            cv2.line(frame, p1, p2, colour, 2)

    writer.write(frame)

    if frame_number % 100 == 0:
        print("Frame", frame_number)

cap.release()
writer.release()

print()
print("Saved to", output_path)
print(f"Tracks with {MIN_TRACK_LENGTH}+ points:")
for track_id, points in sorted(trajectories.items()):
    if len(points) >= MIN_TRACK_LENGTH:
        print(f"  ID {track_id}: {len(points)} points")

# ---- SAVE THE TRAJECTORIES ----
# Units here are PIXELS in the undistorted frame. Not cm. Not metres.
traj_path = "data/output/devwalk_trajectories.json"
with open(traj_path, "w") as f:
    json.dump({str(k): v for k, v in trajectories.items()}, f)
print("Trajectories saved to", traj_path)
print("Track count saved:", len(trajectories))