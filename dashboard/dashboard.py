import streamlit as st
import requests
import pandas as pd 
import streamlit as st


st.set_page_config(
    page_title="Store Intelligence Dashboard",
    layout="wide"
) 



st.title("🛍️ Store Intelligence Dashboard")

# =========================
# API CALLS
# =========================

summary = requests.get(
    "http://127.0.0.1:8000/analytics/summary"
).json()

conversion = requests.get(
    "http://127.0.0.1:8000/analytics/conversion"
).json()

top_zone = requests.get(
    "http://127.0.0.1:8000/analytics/top-zone"
).json()

queue = requests.get(
    "http://127.0.0.1:8000/queue/metrics"
).json()

zones = requests.get(
    "http://127.0.0.1:8000/zones/summary"
).json()

# =========================
# KPI CARDS
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Events",
        summary["total_events"]
    )

with col2:
    st.metric(
        "Entries",
        summary["entries"]
    )

with col3:
    st.metric(
        "Exits",
        summary["exits"]
    )

with col4:
    st.metric(
        "Conversion %",
        conversion["conversion_rate"]
    )

# =========================
# ZONE VISITS
# =========================

st.divider()

st.subheader("📊 Zone Visits")

st.bar_chart(zones)

# =========================
# TOP ZONE
# =========================

st.divider()

st.subheader("🏆 Top Zone")

st.success(
    f"{top_zone['zone']} ({top_zone['visits']} visits)"
)

# =========================
# QUEUE METRICS
# =========================

st.divider()

st.subheader("🛒 Queue Metrics")

q1, q2, q3 = st.columns(3)

with q1:
    st.metric(
        "Average Wait (sec)",
        queue["average_wait_seconds"]
    )

with q2:
    st.metric(
        "Completed Customers",
        queue["completed_customers"]
    )

with q3:
    st.metric(
        "Abandoned Customers",
        queue["abandoned_customers"]
    )

# =========================
# HEATMAP DATA
# =========================

st.divider()

st.subheader("🔥 Heatmap Data")

try:

    heatmap = requests.get(
        "http://127.0.0.1:8000/heatmap/data"
    ).json()

    if heatmap:

        df = pd.DataFrame(heatmap)

        st.dataframe(df)

        if "x" in df.columns and "y" in df.columns:

            st.subheader("Heatmap Scatter Plot")

            st.scatter_chart(
                data=df,
                x="x",
                y="y"
            )

    else:
        st.info("No heatmap data available")

except Exception as e:

    st.error(
        f"Heatmap API Error: {str(e)}"
    )

# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "Store Intelligence Dashboard | YOLOv8 + ByteTrack + FastAPI + Streamlit"
)