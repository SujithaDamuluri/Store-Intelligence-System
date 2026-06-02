from ultralytics import YOLO
import cv2

VIDEO_PATH = "data/videos/CAM 3 - entry.mp4"

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(VIDEO_PATH)

frame_count = 0

while cap.isOpened():
    success, frame = cap.read()

    if not success:
        break

    frame_count += 1

    if frame_count % 5 != 0:
        continue

    results = model(frame, verbose=False)

    annotated_frame = results[0].plot()

    cv2.imshow("YOLO Detection", annotated_frame)

    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()