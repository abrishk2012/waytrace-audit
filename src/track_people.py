import cv2
from ultralytics import YOLO
from collections import defaultdict

video_path = "data/input/test_people.mp4"

model = YOLO("yolo11m.pt")

cap = cv2.VideoCapture(video_path)

start_frame = 1800
max_frames = 500
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
frame_number = 0

seen_ids = set()
frames_per_id = defaultdict(int)

while frame_number < max_frames:
    success, frame = cap.read()
    if not success:
        break

    frame_number += 1

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        imgsz=640,
        conf=0.25,
        classes=[0],
        verbose=False,
    )

    boxes = results[0].boxes

    if boxes.id is not None:
        ids_this_frame = boxes.id.int().tolist()
        for track_id in ids_this_frame:
            seen_ids.add(track_id)
            frames_per_id[track_id] += 1

    if frame_number % 50 == 0:
        print(f"Frame {frame_number} — IDs alive right now: {len(boxes)}")

cap.release()

MIN_TRACK_FRAMES = 25

real_tracks = {}
fragment_tracks = {}

for track_id, length in frames_per_id.items():
    if length >= MIN_TRACK_FRAMES:
        real_tracks[track_id] = length
    else:
        fragment_tracks[track_id] = length

total_person_frames = sum(frames_per_id.values())

print()
print("Frames processed:", frame_number)
print("Total unique IDs created:", len(seen_ids))
print("Average people visible per frame:", round(total_person_frames / frame_number, 2))
print()
print(f"Real tracks (>= {MIN_TRACK_FRAMES} frames): {len(real_tracks)}")
print(f"Fragments  (<  {MIN_TRACK_FRAMES} frames): {len(fragment_tracks)}")
print()
print("Real tracks, longest first:")
for track_id in sorted(real_tracks, key=real_tracks.get, reverse=True):
    seconds = real_tracks[track_id] / 25
    print(f"  ID {track_id}: {real_tracks[track_id]} frames ({seconds:.1f} s)")