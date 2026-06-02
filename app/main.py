from fastapi import FastAPI
from app.schemas import Event
from app.database import EVENTS_DB
from app.data_loader import load_events
from app.routes.analytics import router as analytics_router
app = FastAPI(title="Store Intelligence API")
app.include_router(analytics_router)
@app.get("/")
def home():
    return {
        "message": "Store Intelligence Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "events_loaded": len(EVENTS_DB)
    }


@app.post("/events/ingest")
def ingest_events(events: list[Event]):

    inserted = 0

    for event in events:
        EVENTS_DB.append(event.model_dump())
        inserted += 1

    return {
        "success": True,
        "inserted": inserted,
        "total_events": len(EVENTS_DB)
    }


@app.get("/events")
def get_events():

    return EVENTS_DB

@app.get("/stores/{store_id}/metrics")
def store_metrics(store_id: str):

    entries = 0
    exits = 0

    unique_visitors = set()

    events = load_events()
    for event in events:

        if event.get("store_code") != store_id:
            continue

        unique_visitors.add(event["id_token"])

        if event["event_type"] == "entry":
            entries += 1

        elif event["event_type"] == "exit":
            exits += 1

    conversion_rate = 0

    if entries > 0:
        conversion_rate = round(
            (exits / entries) * 100,
            2
        )

    return {
        "store_id": store_id,
        "unique_visitors": len(unique_visitors),
        "entries": entries,
        "exits": exits,
        "conversion_rate": conversion_rate
    }
    
@app.get("/analytics/summary")
def analytics_summary():

    events = load_events()

    entries = 0
    exits = 0

    for e in events:

        if e.get("event_type") == "entry":
            entries += 1

        elif e.get("event_type") == "exit":
            exits += 1

    return {
        "total_events": len(events),
        "entries": entries,
        "exits": exits
    } 
    
@app.get("/zones/summary")
def zone_summary():

    events = load_events()

    zone_visits = {}

    for event in events:

        if event.get("event_type") == "zone_entered":

            zone = event.get("zone_name", "Unknown")

            if zone not in zone_visits:
                zone_visits[zone] = 0

            zone_visits[zone] += 1

    return zone_visits 

@app.get("/zones/top")
def top_zone():

    events = load_events()

    zone_visits = {}

    for event in events:

        if event.get("event_type") == "zone_entered":

            zone = event.get("zone_name", "Unknown")

            zone_visits[zone] = zone_visits.get(zone, 0) + 1

    if not zone_visits:
        return {"message": "No zone data"}

    top = max(
        zone_visits,
        key=zone_visits.get
    )

    return {
        "top_zone": top,
        "visits": zone_visits[top]
    } 
    
@app.get("/queue/metrics")
def queue_metrics():

    events = load_events()

    waits = []

    abandoned = 0

    for event in events:

        if event.get("event_type") == "queue_completed":
            waits.append(
                event.get("wait_seconds", 0)
            )

        elif event.get("event_type") == "queue_abandoned":
            abandoned += 1

    avg_wait = 0

    if waits:
        avg_wait = round(
            sum(waits) / len(waits),
            2
        )

    return {
        "average_wait_seconds": avg_wait,
        "completed_customers": len(waits),
        "abandoned_customers": abandoned
    } 
    
@app.get("/heatmap/data")
def heatmap_data():

    events = load_events()

    points = []

    for event in events:

        if "zone_hotspot_x" in event:

            points.append({
                "x": event["zone_hotspot_x"],
                "y": event["zone_hotspot_y"],
                "zone": event.get("zone_name", "Unknown")
            })

    return points 

@app.get("/analytics/top-zone")
def top_zone():

    events = load_events()

    zones = {}

    for event in events:

        if event.get("event_type") == "zone_entered":

            zone = event.get(
                "zone_name",
                "Unknown"
            )

            zones[zone] = (
                zones.get(zone, 0) + 1
            )

    if not zones:

        return {
            "zone": "None",
            "visits": 0
        }

    top = max(
        zones,
        key=zones.get
    )

    return {
        "zone": top,
        "visits": zones[top]
    } 
    
@app.get("/analytics/conversion")
def conversion():

    events = load_events()

    entries = 0
    exits = 0

    for event in events:

        if event.get("event_type") == "entry":
            entries += 1

        elif event.get("event_type") == "exit":
            exits += 1

    rate = 0

    if entries > 0:
        rate = round((exits / entries) * 100, 2)

    return {
        "entries": entries,
        "exits": exits,
        "conversion_rate": rate
    }