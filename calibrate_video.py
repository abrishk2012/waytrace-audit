import cv2, numpy as np, os

VIDEO      = "data/raw/2026-08-18_flat_calib.mp4"
CHESSBOARD = (9, 6)
SQUARE_MM  = 19.4
EVERY_N    = 30
TARGET     = 40
BLUR_MIN   = 360.0
CHECK_DIR  = "data/output/calib_check"
os.makedirs(CHECK_DIR, exist_ok=True)

objp = np.zeros((CHESSBOARD[0]*CHESSBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHESSBOARD[0], 0:CHESSBOARD[1]].T.reshape(-1, 2)
objp *= SQUARE_MM

objpoints, imgpoints = [], []
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

cap = cv2.VideoCapture(VIDEO)
if not cap.isOpened():
    raise SystemExit("Could not open video.")

frame_no, tested, kept, size = 0, 0, 0, None
while True:
    ok, frame = cap.read()
    if not ok:
        break
    if frame_no % EVERY_N == 0:
        tested += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if size is None:
            size = gray.shape[::-1]
        found, corners = cv2.findChessboardCorners(
            gray, CHESSBOARD,
            cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE)
        sharp = cv2.Laplacian(gray, cv2.CV_64F).var()
        if found and sharp > BLUR_MIN:
            corners = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            objpoints.append(objp.copy()); imgpoints.append(corners); kept += 1
            print(f"frame {frame_no}: FOUND (kept {kept}) sharp={sharp:.0f}")
    frame_no += 1
cap.release()

print(f"\nFrames read: {frame_no} | tested: {tested} | usable: {kept}")
if kept < 12:
    raise SystemExit("Not enough views. Record a longer clip.")

if len(objpoints) > TARGET:
    idx = np.linspace(0, len(objpoints)-1, TARGET).astype(int)
    objpoints = [objpoints[i] for i in idx]
    imgpoints = [imgpoints[i] for i in idx]
    print(f"Subsampled {kept} views down to {len(objpoints)}, spread across the video")

rms, K, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, size, None, None)
print(f"\nRMS: {rms:.4f} px")
print("K:\n", K)
print("dist:\n", dist.ravel())
np.savez("calibration_ezviz.npz", K=K, dist=dist, size=size, rms=rms, views=len(objpoints))
print("\nSaved calibration_ezviz.npz")