# import_systems.py
# Streamlit dashboard to import infrastructure CSVs and run the ingestion pipeline

import streamlit as st
import pandas as pd
import json
import subprocess
import os
from datetime import datetime

MENTAL_MODEL_PATH = "data/mental_model.json"

st.set_page_config(page_title="🧠 Wisdom Layer Importer", layout="wide")
st.title("📥 Infrastructure Import + CMC Pipeline Runner")

st.markdown("""
Upload infrastructure definitions (servers, networks, etc.) as CSV files. These will be parsed into `events`
and added to your mental model.
""")

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file (e.g., servers.csv)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("CSV loaded successfully!")
    st.dataframe(df)

    events = []
    for _, row in df.iterrows():
        event = {
            "id": row["id"],
            "type": "infrastructure",
            "subtype": "server",
            "hostname": row["hostname"],
            "ip": row["ip"],
            "owner": row["owner"],
            "environment": row["environment"],
            "role": row["role"],
            "timestamp": row.get("timestamp", datetime.utcnow().isoformat())
        }
        events.append(event)

    # Preview events
    st.subheader("🔍 Parsed Events Preview")
    st.json(events)

    if st.button("✅ Append to mental_model.json"):
        if os.path.exists(MENTAL_MODEL_PATH):
            with open(MENTAL_MODEL_PATH, "r") as f:
                model = json.load(f)
        else:
            model = {"events": []}

        existing_ids = {e["id"] for e in model.get("events", [])}
        new_events = [e for e in events if e["id"] not in existing_ids]
        model["events"].extend(new_events)

        with open(MENTAL_MODEL_PATH, "w") as f:
            json.dump(model, f, indent=2)

        st.success(f"Added {len(new_events)} new events to mental_model.json")

# Optionally run the pipeline
st.markdown("---")
st.header("⚙️ Run CMC Pipeline")
if st.button("🚀 Run Pipeline (AI + Orchestration)"):
    try:
        output = subprocess.check_output(["python", "-m", "cmc.run_pipeline"], stderr=subprocess.STDOUT, text=True)
        st.code(output)
        st.success("Pipeline completed successfully.")
    except subprocess.CalledProcessError as e:
        st.error("Pipeline failed.")
        st.code(e.output)
