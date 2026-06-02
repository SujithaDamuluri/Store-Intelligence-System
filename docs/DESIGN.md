# DESIGN.md

## Store Intelligence System - Architecture Design

### Overview

The Store Intelligence System is an AI-powered retail analytics platform designed to extract actionable business insights from CCTV footage. The system processes store camera feeds, detects and tracks customers, generates behavioral events, computes analytics, and presents insights through a dashboard.

---

## System Architecture

```text
CCTV Videos
     |
     v
YOLOv8 Detection
     |
     v
ByteTrack Tracking
     |
     v
Event Generation
     |
     v
generated_events.jsonl
     |
     v
FastAPI Backend
     |
     +--> Analytics APIs
     +--> Queue APIs
     +--> Heatmap APIs
     |
     v
Streamlit Dashboard
```

---

## Detection Layer

The detection layer uses YOLOv8 to identify people in CCTV footage.

Responsibilities:

* Detect customers
* Ignore non-human objects
* Generate bounding boxes
* Provide confidence scores

Input:

* Entry camera footage
* Zone camera footage
* Billing camera footage

Output:

* Person detections

---

## Tracking Layer

ByteTrack is used to assign persistent IDs to detected customers.

Responsibilities:

* Track customers across frames
* Maintain unique visitor identities
* Reduce duplicate counting

Example:

```text
Frame 1 -> Visitor ID 10
Frame 2 -> Visitor ID 10
Frame 3 -> Visitor ID 10
```

---

## Event Generation Layer

Tracked customer movements are converted into business events.

Examples:

* entry
* exit
* zone_entered
* zone_exited
* queue_completed
* queue_abandoned

Events are stored in:

```text
data/events/generated_events.jsonl
```

---

## Analytics Layer

FastAPI provides REST endpoints for business intelligence.

Implemented APIs:

* /events
* /analytics/summary
* /analytics/conversion
* /analytics/top-zone
* /queue/metrics
* /zones/summary
* /heatmap/data

Analytics computed:

* Visitor count
* Conversion rate
* Zone popularity
* Queue performance
* Heatmap coordinates

---

## Dashboard Layer

A Streamlit dashboard visualizes store performance.

Dashboard Features:

* Total Events
* Entries
* Exits
* Conversion Rate
* Zone Visits
* Top Zone
* Queue Metrics
* Heatmap Data

---

## Error Handling

The system handles:

* Missing event files
* Invalid JSON rows
* Empty datasets
* API failures

Graceful fallback responses are returned whenever possible.

---

## Scalability Considerations

Future improvements:

* PostgreSQL storage
* Kafka event streaming
* Multi-store analytics
* Real-time camera feeds
* Cloud deployment

---

## AI-Assisted Decisions

### Decision 1

AI tools were used to compare multiple detection models.

Options considered:

* YOLOv8
* YOLOv9
* RT-DETR

Final choice:

YOLOv8 due to strong accuracy, ease of use, and community support.

### Decision 2

AI-assisted evaluation was used for tracking approaches.

Options considered:

* DeepSORT
* ByteTrack

Final choice:

ByteTrack due to simpler integration and strong tracking performance.

### Decision 3

AI assistance was used to evaluate backend frameworks.

Options considered:

* Flask
* Django
* FastAPI

Final choice:

FastAPI because of automatic Swagger documentation and fast development.
