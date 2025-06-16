import cv2
import numpy as np

# Config
frame_path = "./Data/frame_for_parking.jpg"
spots_path = "./Data/parking_positions.npy"
floor_patch_path = "./Data/floor_reference.npy"
diff_threshold = 27  # Tune this — lower = more strict

# Load assets
frame = cv2.imread(frame_path)
if frame is None:
    raise FileNotFoundError("❌ Cannot load frame image.")

parking_positions = list(np.load(spots_path, allow_pickle=True))
floor_ref = np.load(floor_patch_path)

# Resize floor reference for comparison
floor_ref_resized = cv2.resize(floor_ref, (30, 15))  # Adjust if needed

for polygon in parking_positions:
    pts = np.array(polygon, np.int32).reshape((-1, 1, 2))

    # Create mask
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [pts], 255)

    # Apply mask to get cropped patch
    masked = cv2.bitwise_and(frame, frame, mask=mask)
    x, y, w, h = cv2.boundingRect(pts)
    patch = masked[y:y+h, x:x+w]

    if patch.shape[0] == 0 or patch.shape[1] == 0:
        continue

    # Resize both patches to same size
    patch_resized = cv2.resize(patch, (30, 15))

    # Compute mean absolute color difference
    diff = cv2.absdiff(patch_resized, floor_ref_resized)
    mean_diff = np.mean(diff)

    # Decide if spot is occupied
    color = (0, 255, 0) if mean_diff < diff_threshold else (0, 0, 255)

    # Draw outline
    cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=2)
    cv2.putText(frame, f"{int(mean_diff)}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

# Show result 
cv2.imshow("Parking Detection (Floor Ref)", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()