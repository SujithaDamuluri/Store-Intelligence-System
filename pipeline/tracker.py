from ultralytics import YOLO
import supervision as sv
import cv2

VIDEO_PATH = "data/videos/CAM 3 - entry.mp4"

model = YOLO("yolov8n.pt")

tracker = sv.ByteTrack()

cap = cv2.VideoCapture(VIDEO_PATH)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    result = model(frame, verbose=False)[0]

    detections = sv.Detections.from_ultralytics(result)

    detections = tracker.update_with_detections(detections)

    annotated = frame.copy()

    if detections.tracker_id is not None:

        for i, box in enumerate(detections.xyxy):

            x1, y1, x2, y2 = map(int, box)

            track_id = detections.tracker_id[i]

            print("DRAWING ID:", track_id)

            cv2.rectangle(
                annotated,
                (x1, y1),
                (x2, y2),
                (255, 0, 255),
                2
            )

            cv2.putText(
    annotated,
    f"ID {track_id}",
    (50, 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    2,
    (0, 0, 255),
    5
)

    cv2.imshow("Visitor Tracking", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()