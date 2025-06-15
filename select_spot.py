import cv2
import numpy as np
import os

# File paths
image_path = "./Data/frame_for_parking.jpg"         # Image used for selecting parking spots
output_file = "./Data/parking_positions.npy"        # File to save selected parking spots

# Load the image
img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError(f"❌ Could not find {image_path}")

# Load existing parking positions if file exists
parking_positions = []
if os.path.exists(output_file):
    parking_positions = list(np.load(output_file, allow_pickle=True))

# Temporary list to hold a polygon while it's being drawn
current_polygon = []

# Mouse event callback
def mouse_click(event, x, y, flags, param):
    global current_polygon, parking_positions

    # Left-click to add a point
    if event == cv2.EVENT_LBUTTONDOWN:
        current_polygon.append((x, y))
        # When 4 points are selected, add as a complete parking spot polygon
        if len(current_polygon) == 4:
            parking_positions.append(current_polygon.copy())
            current_polygon = []

    # Right-click to remove the most recently saved polygon
    elif event == cv2.EVENT_RBUTTONDOWN:
        if parking_positions:
            parking_positions.pop()

# Create window and set mouse callback
cv2.namedWindow("Parking Spot Selector")
cv2.setMouseCallback("Parking Spot Selector", mouse_click)

# Main loop to draw and update GUI
while True:
    img_copy = img.copy()

    # Draw all saved polygons (parking spots)
    for polygon in parking_positions:
        pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
        cv2.polylines(img_copy, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

    # Draw points for the currently selected (in-progress) polygon
    for pt in current_polygon:
        cv2.circle(img_copy, pt, 4, (255, 0, 0), -1)

    # Display the frame
    cv2.imshow("Parking Spot Selector", img_copy)
    key = cv2.waitKey(1)

    # Press 's' to save parking positions
    if key == ord('s'):
        np.save(output_file, parking_positions)

        # Save summary to text file
        with open("./Data/parking_summary.txt", "w") as f:
            f.write(f"Total parking spots selected: {len(parking_positions)}\n")

        print(f"✅ Saved {len(parking_positions)} spots to '{output_file}'")
        print("📄 Summary saved to 'parking_summary.txt'")
        break

    # Press 'q' to quit without saving
    elif key == ord('q'):
        print("❌ Exited without saving")
        break

# Close the OpenCV window
cv2.destroyAllWindows()