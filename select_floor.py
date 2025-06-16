import cv2
import numpy as np

image_path = "./Data/frame_for_parking.jpg"
output_image = "./Data/floor_reference.jpg"
output_array = "./Data/floor_reference.npy"

# Load image
img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError(f"❌ Could not find {image_path}")

ref_polygon = []

def mouse_click(event, x, y, flags, param):
    global ref_polygon
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_polygon.append((x, y))

# Set up window
cv2.namedWindow("Select Floor Reference")
cv2.setMouseCallback("Select Floor Reference", mouse_click)

print("🖱️ Click 4 points to select a clean floor polygon.")
while True:
    img_copy = img.copy()

    # Draw clicked points
    for pt in ref_polygon:
        cv2.circle(img_copy, pt, 4, (255, 0, 0), -1)

    # Draw polygon if 4 points selected
    if len(ref_polygon) == 4:
        pts = np.array(ref_polygon, np.int32).reshape((-1, 1, 2))
        cv2.polylines(img_copy, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

    cv2.imshow("Select Floor Reference", img_copy)
    key = cv2.waitKey(1)

    if key == ord('s') and len(ref_polygon) == 4:
        # Create mask for the polygon
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        pts = np.array(ref_polygon, np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(mask, [pts], 255)

        # Apply mask to image
        masked = cv2.bitwise_and(img, img, mask=mask)

        # Crop to bounding box of polygon
        x, y, w, h = cv2.boundingRect(pts)
        patch = masked[y:y+h, x:x+w]

        # Save results
        cv2.imwrite(output_image, patch)
        np.save(output_array, patch)
        print(f"✅ Saved floor reference to:\n - {output_image}\n - {output_array}")
        break

    elif key == ord('q'):
        print("❌ Quit without saving.")
        break

cv2.destroyAllWindows()