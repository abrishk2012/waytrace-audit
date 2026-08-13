import cv2
from ultralytics import YOLO

video_path = "data/input/test_people.mp4"
output_path = "data/output/first_detection.jpg"

model = YOLO("yolo11n.pt")

cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, 2000)
success, frame = cap.read()
cap.release()

if not success:
    print("ERROR: could not read frame 2000")
    exit()

results = model(frame, imgsz=960, conf=0.25, classes=[0])

boxes = results[0].boxes
print("People found:", len(boxes))

for box in boxes:
    x1, y1, x2, y2 = box.xyxy[0]
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    confidence = float(box.conf[0])

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(frame, f"{confidence:.2f}", (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

cv2.imwrite(output_path, frame)
print("Saved to", output_path)