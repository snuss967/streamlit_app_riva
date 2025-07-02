#!/usr/bin/env python3
"""
Fetch the current page‑view count for Federal Register document 2025‑12347 and append
(timestamp, count) to a local CSV file (data.csv).

Designed to be executed by a GitHub Actions workflow every hour.
"""
import os
import sys
from datetime import datetime, timezone

import pandas as pd
import requests

DATA_FILE = "data.csv"
API_URL = (
    "https://www.federalregister.gov/api/v1/public_inspection_documents/2025-12347.json"
)

def get_view_count() -> int:
    """Return the current view‑count for the target document."""
    resp = requests.get(API_URL, timeout=30)
    resp.raise_for_status()
    return resp.json().get("page_views", {}).get("count")
    
def append_result(count: int) -> None:
    """Append (timestamp, count) to DATA_FILE, creating it if necessary."""
    ts = datetime.now(timezone.utc).isoformat()
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["timestamp", "count"])

    df = pd.concat(
        [df, pd.DataFrame([{"timestamp": ts, "count": count}])],
        ignore_index=True,
    )
    df.to_csv(DATA_FILE, index=False)
    print(f"Appended {count} at {ts}")

def main() -> None:
    try:
        count = get_view_count()
        append_result(count)
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()
