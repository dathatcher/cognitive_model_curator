# 📊 Model Completeness Assistant for Wisdom Layer
# Scans systems_model.json and presents enrichment suggestions

import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="🧠 Model Completeness Assistant", page_icon="📊")
st.title("🧠 Model Completeness Assistant")

project_dirs = sorted(Path("projects").glob("*/"))
if not project_dirs:
    st.error("⚠️ No projects found in 'projects/' folder.")
    st.stop()

project_selection = st.selectbox("📂 Select a project:", [p.name for p in project_dirs])
project_dir = Path("projects") / project_selection
systems_model_path = project_dir / "systems_model.json"

if not systems_model_path.exists():
    st.error("❌ systems_model.json not found in selected project.")
    st.stop()

with open(systems_model_path) as f:
    model = json.load(f)

st.subheader("🔍 Distinctions Missing Data")
empty_distinctions = {k: v for k, v in model.items() if isinstance(v, list) and not v and k != "Agent_Insights"}
if empty_distinctions:
    for d in empty_distinctions:
        st.warning(f"➖ {d} has no entries")
else:
    st.success("✅ All distinctions have at least one entry")

st.divider()

st.subheader("🧠 DSRP Completeness Gaps")
dsrp_entities = set()
for insight in model.get("Agent_Insights", {}).get("DSRP", []):
    dsrp_entities.update(insight.get("related_entities", []))

for distinction in model:
    if distinction in ["Agent_Insights"] or not isinstance(model[distinction], list):
        continue
    for item in model[distinction]:
        name = item.get("name")
        if name and name not in dsrp_entities:
            st.info(f"🔹 {name} in '{distinction}' is **not referenced in any DSRP insight**")

st.divider()

st.subheader("📉 Weak Coverage in Chaos or Karma")
chaos_refs = set()
for insight in model.get("Agent_Insights", {}).get("Chaos", []):
    chaos_refs.update(insight.get("trigger_elements", []) + insight.get("impacted_elements", []))

karma_refs = set()
for insight in model.get("Agent_Insights", {}).get("Karma", []):
    karma_refs.update(insight.get("affected_roles", []) + insight.get("referenced_rules", []))

for distinction in model:
    if distinction in ["Agent_Insights"] or not isinstance(model[distinction], list):
        continue
    for item in model[distinction]:
        name = item.get("name")
        if name:
            if name not in chaos_refs:
                st.warning(f"🌪️ {name} missing from Chaos insights")
            if name not in karma_refs:
                st.warning(f"⚖️ {name} missing from Karma insights")
