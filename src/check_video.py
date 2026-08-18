import cv2

video_path = "data/output/tracked_preview.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("ERROR: OpenCV could not open the video.")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
reported_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print("FPS:", fps)
print("Size:", width, "x", height)
print("Frames the file claims to have:", reported_frames)
print("Length in seconds:", round(reported_frames / fps, 1))

frames_read = 0
while True:
    success, frame = cap.read()
    if not success:
        break
    frames_read += 1

print("Frames actually read:", frames_read)

cap.release()
print("Done.")