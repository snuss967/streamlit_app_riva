import os
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

DATA_FILE = "data.csv"
DOC_NUM = "2025-12347"

st.set_page_config(page_title="Federal Register View Tracker", layout="wide")
st.title("Federal Register View Tracker")
st.write(f"Tracking page views for document **{DOC_NUM}**. Data is updated hourly via GitHub Actions.")

if not os.path.exists(DATA_FILE):
    st.warning("No data collected yet. The first GitHub Actions run will populate `data.csv` within the next hour.")
    st.stop()

# Load & prepare data
_df = pd.read_csv(DATA_FILE)
_df["timestamp"] = pd.to_datetime(_df["timestamp"], utc=True)
_df = _df.set_index("timestamp")

latest_ts = _df.index[-1]
latest_count = _df["count"].iloc[-1]

st.metric(label="Current page views (latest)", value=latest_count, delta=None)

st.line_chart(_df["count"], use_container_width=True)

st.caption(f"Last updated: {latest_ts.strftime('%Y-%m-%d %H:%M UTC')}")
