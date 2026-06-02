from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/analytics/top-zone")
def top_zone():

    try:
        with open("data/events/generated_events.jsonl", "r") as f:
            events = [json.loads(line) for line in f]

    except:
        return {"zone": "None", "visits": 0}

    zone_counts = {}

    for event in events:

        if event.get("event_type") == "zone_entered":

            zone = event.get("zone_name")

            zone_counts[zone] = zone_counts.get(zone, 0) + 1

    if not zone_counts:
        return {"zone": "None", "visits": 0}

    best_zone = max(zone_counts, key=zone_counts.get)

    return {
        "zone": best_zone,
        "visits": zone_counts[best_zone]
    }