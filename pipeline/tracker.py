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
    print("Tracker IDs:", detections.tracker_id)
    labels = []

    if detections.tracker_id is not None:
        for track_id in detections.tracker_id:
            labels.append(f"ID {track_id}")

    annotated = frame.copy()

    box_annotator = sv.BoxAnnotator()

    annotated = box_annotator.annotate(
        scene=annotated,
        detections=detections
    )

    label_annotator = sv.LabelAnnotator()

    annotated = label_annotator.annotate(
        scene=annotated,
        detections=detections,
        labels=labels
    )

    cv2.imshow("Visitor Tracking", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()