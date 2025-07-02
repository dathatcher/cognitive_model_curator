import streamlit as st
import json
from pathlib import Path
from openai import OpenAI
from glob import glob
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Systems Thinking Agent (DSRP)", page_icon="🔄")
st.title("🔄 Systems Thinking Agent: DSRP Insight Generator")

# 🔽 Select project folder
project_dirs = sorted(glob("projects/*"))
if not project_dirs:
    st.error("⚠️ No projects found in 'projects/' folder.")
    st.stop()

project_name_map = {Path(p).name: p for p in project_dirs}
project_selection = st.selectbox("📂 Select a project:", list(project_name_map.keys()))
project_dir = Path(project_name_map[project_selection])
systems_model_path = project_dir / "systems_model.json"

if not systems_model_path.exists():
    st.error("⚠️ systems_model.json not found in the selected project.")
    st.stop()

# ✅ Load model data
with open(systems_model_path, "r") as f:
    model_data = json.load(f)

all_distinctions = list(model_data.keys())
selected_distinctions = st.multiselect("🧠 Select distinctions to analyze with DSRP:", all_distinctions, default=["Roles", "Rules"])

filtered_data = {k: v for k, v in model_data.items() if k in selected_distinctions}

if st.button("🌀 Generate DSRP Systems Insights"):
    with st.spinner("Analyzing systemic structure using DSRP..."):
        prompt = f"""
You are the Systems Thinking Agent. Apply the DSRP framework (Distinctions, Systems, Relationships, Perspectives) to the following Complex Adaptive System (CAS) data.

Distinctions selected: {selected_distinctions}

Data:
{json.dumps(filtered_data, indent=2)}

For each insight:
- Describe the **systemic insight** observed
- Tag the relevant DSRP **elements** (choose from: Distinction, System, Relationship, Perspective)
- List any **related entities** mentioned in the insight

Return a JSON array like:
[
  {{
    "insight": "...",
    "dsrp_elements": ["Distinction", "Relationship"],
    "related_entities": ["Mother", "Curfew Policy"]
  }},
  ...
]

Do not include any extra explanation or markdown.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a DSRP systems thinking analyst."},
                    {"role": "user", "content": prompt}
                ]
            )
            insights = response.choices[0].message.content.strip()
            st.markdown("### 🔍 DSRP-Based Systems Insights")
            st.code(insights, language="json")

            try:
                parsed = json.loads(insights)

                # Save standalone file
                output_path = project_dir / "systems_thinking_insights.json"
                with open(output_path, "w") as f:
                    json.dump(parsed, f, indent=2)

                # Embed into systems_model.json
                if "Agent_Insights" not in model_data:
                    model_data["Agent_Insights"] = {}

                model_data["Agent_Insights"]["DSRP"] = parsed

                with open(systems_model_path, "w") as f:
                    json.dump(model_data, f, indent=2)

                st.success(f"✅ DSRP insights saved to: {output_path} and embedded in model.")
            except Exception as parse_err:
                st.warning("⚠️ Could not parse output. Please review raw response.")

        except Exception as e:
            st.error(f"OpenAI API error: {e}")
