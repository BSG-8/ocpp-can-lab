import streamlit as st
import pandas as pd

import sys
import os

# Add project root to sys.path to allow importing log_viewer as a package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from log_viewer.parser import list_runs, load_events


st.set_page_config(
    page_title="OCPP–CAN Log Viewer",
    layout="wide"
)

st.title(" OCPP–CAN Global Log Viewer")
st.caption("Read-only visualization of simulation runs")


st.sidebar.header("Simulation Runs")

runs = list_runs()

if not runs:
    st.warning("No simulation runs found in logs/")
    st.stop()

selected_run = st.sidebar.selectbox(
    "Select a run",
    runs,
    index=len(runs) - 1  # default: latest run
)


run_path = f"logs/{selected_run}"

with st.spinner("Loading events..."):
    events, scenario_name = load_events(run_path)

if not events:
    st.warning("No events found for this run.")
    st.stop()

st.markdown(
    f"**🧪 Active Scenario:** `{scenario_name}`"
)




data = []
for e in events:
    data.append({
        "timestamp": e.ts,
        "source": e.source,
        "action": e.action,
        "message": e.message,
        "direction": e.direction,
        "raw": e.data,
    })

df = pd.DataFrame(data)


st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:
    sources = sorted(df["source"].dropna().unique().tolist())
    selected_sources = st.multiselect(
        "Source",
        sources,
        default=sources
    )

with col2:
    keyword = st.text_input("Search keyword")


filtered_df = df[df["source"].isin(selected_sources)]

if keyword:
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: keyword.lower() in str(row).lower(),
            axis=1
        )
    ]


# Reset index to make sure 0..N matches the selection
filtered_df = filtered_df.reset_index(drop=True)


st.subheader(f"Events ({len(filtered_df)})")

# Add a visible column for index
display_df = filtered_df.copy()
display_df.insert(0, "#", display_df.index)

st.dataframe(
    display_df.drop(columns=["raw"]),
    use_container_width=True,
    height=400
)


st.subheader("Inspect Event")

selected_index = st.selectbox(
    "Select an event to inspect details",
    options=list(filtered_df.index),
    format_func=lambda i: f"{i} | {filtered_df.loc[i, 'timestamp']} | {filtered_df.loc[i, 'action']}"
)

selected_event = filtered_df.loc[selected_index]
st.json(selected_event["raw"])



