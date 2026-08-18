import cv2, sys

if len(sys.argv) < 2:
    print("Usage: python src/check_video.py <path-to-video>")
    sys.exit(1)

video_path = sys.argv[1]
print("Checking:", video_path)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("ERROR: OpenCV could not open the video.")
    sys.exit(1)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
reported = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print("FPS:", fps)
print("Size:", width, "x", height)
print("Frames the file claims to have:", reported)

frames_read = 0
while True:
    success, frame = cap.read()
    if not success:
        break
    frames_read += 1
cap.release()

print("Frames actually read:", frames_read)
print("Length in seconds:", round(frames_read / fps, 1) if fps else "unknown")
if reported != frames_read:
    print(f"WARNING: header claims {reported}, real count is {frames_read}")
print("Done.")