import os
from datetime import datetime, timezone

import pandas as pd
import altair as alt
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

max_count = _df["count"].max()
chart = (
    alt.Chart(_df.reset_index())
    .mark_line()
    .encode(
        x=alt.X("timestamp:T", title="Timestamp"),
        y=alt.Y(
            "count:Q",
            title="Page Views",
            scale=alt.Scale(domain=[500, max_count + 10]),
        ),
        tooltip=["timestamp:T", "count:Q"],
    )
)
st.altair_chart(chart, use_container_width=True)

st.caption(f"Last updated: {latest_ts.strftime('%Y-%m-%d %H:%M UTC')}")
