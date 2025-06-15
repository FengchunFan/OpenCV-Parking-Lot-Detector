# Capture a frame (image) from target video

import cv2

# Target footage
video_path = ".\Data\cliped_footage.mp4"
cap = cv2.VideoCapture(video_path)

# Capture first frame of video footage
frame_id = 0
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)

# Verify the capture
success, frame = cap.read()
if success:
    cv2.imwrite("./Data/frame_for_parking.jpg", frame)
    print("✅ Frame captured and saved successfully")
else:
    print("❌ Failed to capture frame")

cap.release()
