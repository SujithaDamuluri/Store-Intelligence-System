import requests
import streamlit as st

st.title("Store Intelligence Dashboard")

summary = requests.get(
    "http://127.0.0.1:8000/analytics/summary"
).json()

st.subheader("Store Summary")

st.write(summary)

zones = requests.get(
    "http://127.0.0.1:8000/zones/summary"
).json()

st.subheader("Zone Visits")

st.bar_chart(zones)

queue = requests.get(
    "http://127.0.0.1:8000/queue/metrics"
).json()

st.subheader("Queue Metrics")

st.write(queue)