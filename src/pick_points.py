import cv2

IMG = "data/output/floor_undistorted.jpg"
points = []

def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        print("Point", len(points), "=", x, y)
        cv2.circle(display, (x, y), 4, (0, 0, 255), -1)
        cv2.imshow("Click 4 corners", display)

img = cv2.imread(IMG)
if img is None:
    raise SystemExit("Could not read " + IMG)

display = img.copy()
cv2.namedWindow("Click 4 corners")
cv2.setMouseCallback("Click 4 corners", on_click)
cv2.imshow("Click 4 corners", display)

print("Click in this order: bottom-left, bottom-right, top-right, top-left")
print("Then press any key to close.")

cv2.waitKey(0)
cv2.destroyAllWindows()

print()
print("Your 4 points:")
print(points)