import cv2

VIDEO = "data/raw/2026-08-19_flat_camC_empty.mp4"
OUT = "data/output/floor_raw.jpg"
GRAB_AT = 200

cap = cv2.VideoCapture(VIDEO)
count = 0
saved = False

while True:
    ok, frame = cap.read()
    if not ok:
        break
    if count == GRAB_AT:
        cv2.imwrite(OUT, frame)
        saved = True
        print("Saved frame", count, "to", OUT)
    count += 1

cap.release()
print("Total frames read:", count)
if not saved:
    print("WARNING: never reached frame", GRAB_AT)