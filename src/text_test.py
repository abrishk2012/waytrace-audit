import cv2, numpy as np
img = np.full((300, 900, 3), 60, np.uint8)
cv2.putText(img, "WayTrace friction hotspots", (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
cv2.putText(img, "WayTrace friction hotspots", (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 2)
cv2.putText(img, "WayTrace friction hotspots", (20, 220),
            cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255,255,255), 3)
cv2.imwrite("data/output/text_test.png", img)
print("written")
