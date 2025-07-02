import streamlit as st
import json
from pathlib import Path
from openai import OpenAI
from glob import glob
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Complexity Sentinel Agent", page_icon="🧠")
st.title("🧠 Complexity Sentinel: Complexity Insight Detector")

# 🔽 Project Picker
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

# ✅ Load current model
with open(systems_model_path, "r") as f:
    model_data = json.load(f)

all_distinctions = list(model_data.keys())
selected_distinctions = st.multiselect(
    "🔍 Select distinctions to analyze for complexity feedback and interactions:",
    all_distinctions,
    default=["Roles", "Rules"]
)

filtered_data = {k: v for k, v in model_data.items() if k in selected_distinctions}

if st.button("📡 Detect Complexity Patterns"):
    with st.spinner("Scanning system structure and relationships..."):
        prompt = f"""
You are the Complexity Sentinel Agent. Analyze the following distinctions from a systems model to identify signs of complexity, including:

- Interdependencies
- Feedback loops
- Emergent behavior
- Ripple effects from roles or rules
- Signals of potential systemic fragility

Selected Distinctions: {selected_distinctions}

Data:
{json.dumps(filtered_data, indent=2)}

For each insight:
- Describe the observed or potential complexity pattern
- List any related distinctions, roles, or rules involved
- Indicate whether it suggests stability, fragility, or unpredictability

Return JSON in this format:
[
  {{
    "insight": "...",
    "related_elements": ["..."],
    "complexity_signal": "fragility"  // or "stability", "unpredictability"
  }}
]
Do not include any explanation or markdown.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a Complexity Sentinel Agent detecting systemic feedback and fragility."},
                    {"role": "user", "content": prompt}
                ]
            )
            insights = response.choices[0].message.content.strip()
            st.markdown("### 🕸️ Complexity Insights")
            st.code(insights, language="json")

            try:
                parsed = json.loads(insights)

                # Save to file
                output_path = project_dir / "complexity_insights.json"
                with open(output_path, "w") as f:
                    json.dump(parsed, f, indent=2)

                # Embed into model
                if "Agent_Insights" not in model_data:
                    model_data["Agent_Insights"] = {}
                model_data["Agent_Insights"]["Complexity"] = parsed

                with open(systems_model_path, "w") as f:
                    json.dump(model_data, f, indent=2)

                st.success(f"✅ Complexity insights saved to: {output_path} and embedded in model.")
            except Exception as parse_err:
                st.warning("⚠️ Could not parse output. Please review raw response.")

        except Exception as e:
            st.error(f"OpenAI API error: {e}")
