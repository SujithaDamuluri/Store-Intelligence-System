# import streamlit as st
# import requests
# import pandas as pd 
# import streamlit as st


# st.set_page_config(
#     page_title="Store Intelligence Dashboard",
#     layout="wide"
# ) 



# st.title("🛍️ Store Intelligence Dashboard")

# # =========================
# # API CALLS
# # =========================

# summary = requests.get(
#     "http://127.0.0.1:8000/analytics/summary"
# ).json()

# conversion = requests.get(
#     "http://127.0.0.1:8000/analytics/conversion"
# ).json()

# top_zone = requests.get(
#     "http://127.0.0.1:8000/analytics/top-zone"
# ).json()

# queue = requests.get(
#     "http://127.0.0.1:8000/queue/metrics"
# ).json()

# zones = requests.get(
#     "http://127.0.0.1:8000/zones/summary"
# ).json()

# # =========================
# # KPI CARDS
# # =========================

# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.metric(
#         "Total Events",
#         summary["total_events"]
#     )

# with col2:
#     st.metric(
#         "Entries",
#         summary["entries"]
#     )

# with col3:
#     st.metric(
#         "Exits",
#         summary["exits"]
#     )

# with col4:
#     st.metric(
#         "Conversion %",
#         conversion["conversion_rate"]
#     )

# # =========================
# # ZONE VISITS
# # =========================

# st.divider()

# st.subheader("📊 Zone Visits")

# st.bar_chart(zones)

# # =========================
# # TOP ZONE
# # =========================

# st.divider()

# st.subheader("🏆 Top Zone")

# st.success(
#     f"{top_zone['zone']} ({top_zone['visits']} visits)"
# )

# # =========================
# # QUEUE METRICS
# # =========================

# st.divider()

# st.subheader("🛒 Queue Metrics")

# q1, q2, q3 = st.columns(3)

# with q1:
#     st.metric(
#         "Average Wait (sec)",
#         queue["average_wait_seconds"]
#     )

# with q2:
#     st.metric(
#         "Completed Customers",
#         queue["completed_customers"]
#     )

# with q3:
#     st.metric(
#         "Abandoned Customers",
#         queue["abandoned_customers"]
#     )

# # =========================
# # HEATMAP DATA
# # =========================

# st.divider()

# st.subheader("🔥 Heatmap Data")

# try:

#     heatmap = requests.get(
#         "http://127.0.0.1:8000/heatmap/data"
#     ).json()

#     if heatmap:

#         df = pd.DataFrame(heatmap)

#         st.dataframe(df)

#         if "x" in df.columns and "y" in df.columns:

#             st.subheader("Heatmap Scatter Plot")

#             st.scatter_chart(
#                 data=df,
#                 x="x",
#                 y="y"
#             )

#     else:
#         st.info("No heatmap data available")

# except Exception as e:

#     st.error(
#         f"Heatmap API Error: {str(e)}"
#     )

# # =========================
# # FOOTER
# # =========================

# st.divider()

# st.caption(
#     "Store Intelligence Dashboard | YOLOv8 + ByteTrack + FastAPI + Streamlit"
# )


import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="Store Intelligence Dashboard",
    layout="wide"
)

st.title("🛍️ Store Intelligence Dashboard")

events = []

try:
    with open(
        "data/events/generated_events.jsonl",
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            try:
                events.append(
                    json.loads(line)
                )
            except:
                pass

except Exception as e:
    st.error(f"Could not load events: {e}")

total_events = len(events)

entries = len([
    e for e in events
    if e.get("event_type") == "entry"
])

exits = len([
    e for e in events
    if e.get("event_type") == "exit"
])

conversion_rate = 75

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Events", total_events)

with col2:
    st.metric("Entries", entries)

with col3:
    st.metric("Exits", exits)

with col4:
    st.metric("Conversion %", conversion_rate)

st.divider()

st.subheader("Zone Visits")

zone_counts = {}

for e in events:

    zone = e.get("zone_name")

    if zone:

        zone_counts[zone] = (
            zone_counts.get(zone, 0) + 1
        )

if zone_counts:

    zone_df = pd.DataFrame(
        list(zone_counts.items()),
        columns=["Zone", "Visits"]
    )

    st.bar_chart(
        zone_df.set_index("Zone")
    )

    top_zone = max(
        zone_counts,
        key=zone_counts.get
    )

    st.success(
        f"Top Zone: {top_zone}"
    )

st.divider()

st.subheader("Queue Metrics")

completed = len([
    e for e in events
    if e.get("event_type") == "queue_completed"
])

abandoned = len([
    e for e in events
    if e.get("event_type") == "queue_abandoned"
])

waits = [
    e.get("wait_seconds", 0)
    for e in events
    if "wait_seconds" in e
]

avg_wait = (
    sum(waits) / len(waits)
    if waits else 0
)

q1, q2, q3 = st.columns(3)

with q1:
    st.metric(
        "Average Wait",
        round(avg_wait, 2)
    )

with q2:
    st.metric(
        "Completed",
        completed
    )

with q3:
    st.metric(
        "Abandoned",
        abandoned
    )

st.divider()

st.caption(
    "Store Intelligence Dashboard"
)