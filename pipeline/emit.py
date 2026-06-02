import json
from datetime import datetime

OUTPUT_FILE = "data/events/generated_events.jsonl"


def emit_event(event):

    with open(OUTPUT_FILE, "a") as f:

        f.write(
            json.dumps(event) + "\n"
        )


sample_event = {
    "event_type": "entry",
    "id_token": "ID_10",
    "store_code": "store_1",
    "camera_id": "CAM3",
    "event_timestamp": datetime.now().isoformat(),
    "is_staff": False
}

emit_event(sample_event)

print("Event Written")