import cv2
import numpy as np

# Config
video_path = "./Data/cliped_footage.mp4"
spots_path = "./Data/parking_positions.npy"
floor_patch_path = "./Data/floor_reference.npy"
diff_threshold = 27
target_size = (30, 15)

# Load reference patch and parking spots 
floor_ref = np.load(floor_patch_path)
floor_ref_resized = cv2.resize(floor_ref, target_size)
parking_positions = list(np.load(spots_path, allow_pickle=True))

# Open video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise FileNotFoundError(f"❌ Could not open {video_path}")

# Optional: Save output
save_output = False
if save_output:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('./Data/parking_detection_output.mp4', fourcc, 20.0,
                          (int(cap.get(3)), int(cap.get(4))))

# Process frames 
while True:
    success, frame = cap.read()
    if not success:
        break

    for polygon in parking_positions:
        pts = np.array(polygon, np.int32).reshape((-1, 1, 2))

        # Create mask
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [pts], 255)

        # Crop the spot
        masked = cv2.bitwise_and(frame, frame, mask=mask)
        x, y, w, h = cv2.boundingRect(pts)
        patch = masked[y:y+h, x:x+w]

        if patch.shape[0] == 0 or patch.shape[1] == 0:
            continue

        patch_resized = cv2.resize(patch, target_size)

        # Color difference
        diff = cv2.absdiff(patch_resized, floor_ref_resized)
        mean_diff = np.mean(diff)

        # Decision
        color = (0, 255, 0) if mean_diff < diff_threshold else (0, 0, 255)

        # Draw results
        cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=2)
        cv2.putText(frame, f"{int(mean_diff)}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    cv2.imshow("Parking Detection (Video)", frame)
    if save_output:
        out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if save_output:
    out.release()
cv2.destroyAllWindows()