import cv2
from ultralytics import YOLO

video_path = "data/input/tilt_test_cfr.mp4"
output_path = "data/output/tracked_preview.mp4"

START_FRAME = 0
MAX_FRAMES = 300

model = YOLO("yolo11m.pt")

cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, START_FRAME)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))


def colour_for_id(track_id):
    return (
        (track_id * 67) % 255,
        (track_id * 131) % 255,
        (track_id * 197) % 255,
    )


frame_number = 0

while frame_number < MAX_FRAMES:
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
        for box, track_id in zip(boxes.xyxy, boxes.id.int().tolist()):
            x1, y1, x2, y2 = [int(v) for v in box]
            colour = colour_for_id(track_id)

            cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)
            cv2.putText(frame, f"#{track_id}", (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 2)

            foot_x = (x1 + x2) // 2
            foot_y = y2
            cv2.circle(frame, (foot_x, foot_y), 4, colour, -1)

    writer.write(frame)

    if frame_number % 100 == 0:
        print("Written frame", frame_number)

cap.release()
writer.release()
print("Saved to", output_path)