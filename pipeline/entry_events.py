from ultralytics import YOLO
import supervision as sv
import cv2
from collections import defaultdict

VIDEO_PATH = "data/videos/CAM 3 - entry.mp4"

model = YOLO("yolov8n.pt")
tracker = sv.ByteTrack()

cap = cv2.VideoCapture(VIDEO_PATH)

line_x = 1100

previous_side = {}

while True:

    ret, frame = cap.read()

    if not ret:
        break

    result = model(frame, verbose=False)[0]

    detections = sv.Detections.from_ultralytics(result)
    detections = tracker.update_with_detections(detections)

    cv2.line(
        frame,
        (line_x, 0),
        (line_x, frame.shape[0]),
        (0, 255, 255),
        3
    )

    if detections.tracker_id is not None:

        for i, bbox in enumerate(detections.xyxy):

            x1, y1, x2, y2 = bbox

            center_x = int((x1 + x2) / 2)

            track_id = int(detections.tracker_id[i])

            current_side = "LEFT" if center_x < line_x else "RIGHT"
            print(f"ID={track_id} center_x={center_x} side={current_side}")
            if track_id in previous_side:

                old_side = previous_side[track_id]

                if old_side == "RIGHT" and current_side == "LEFT":
                    print(f"ENTRY -> ID_{track_id}")

                elif old_side == "LEFT" and current_side == "RIGHT":
                    print(f"EXIT -> ID_{track_id}")

            previous_side[track_id] = current_side

            cv2.rectangle(
                frame,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"ID {track_id}",
                (int(x1), int(y1)-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2
            )

    cv2.imshow("Entry Detection", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()