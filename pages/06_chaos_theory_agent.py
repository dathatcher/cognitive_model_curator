import streamlit as st
import json
from pathlib import Path
from openai import OpenAI
from glob import glob
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Chaos Theory Agent")
st.title("🌀 Chaos Theory Agent: Ripple Effect Analyzer")

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
    "🔄 Select distinctions to analyze ripple and chaos effects:",
    all_distinctions,
    default=["Roles", "Rules"]
)

filtered_data = {k: v for k, v in model_data.items() if k in selected_distinctions}

if st.button("🌪️ Detect Chaos Patterns"):
    with st.spinner("Tracing chaotic interactions and ripple chains..."):
        prompt = f"""
You are the Chaos Theory Agent. Analyze the following distinctions to uncover patterns of chaos theory within this Complex Adaptive System (CAS).

Focus on:
- Ripple effects and cascading consequences
- Butterfly effects (small inputs → large outcomes)
- Delay-amplified feedback loops
- Sensitive dependence on initial conditions
- Nonlinear chain reactions

Selected Distinctions: {selected_distinctions}

Data:
{json.dumps(filtered_data, indent=2)}

For each insight:
- Describe the **chaotic insight**
- Identify **trigger elements** (e.g. rules, roles, events)
- Identify **impacted elements** (e.g. tools, teams, individuals)
- Tag with a **volatility_type** (ripple, feedback, amplification, delay, sensitivity)

Return JSON array like:
[
  {{
    "insight": "...",
    "trigger_elements": ["..."],
    "impacted_elements": ["..."],
    "volatility_type": "ripple"
  }}
]
Do not include explanation or markdown.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a Chaos Theory Agent analyzing nonlinear interactions and ripple effects."},
                    {"role": "user", "content": prompt}
                ]
            )
            insights = response.choices[0].message.content.strip()
            st.markdown("### 🌪️ Chaos Insights")
            st.code(insights, language="json")

            try:
                parsed = json.loads(insights)

                # Save to file
                output_path = project_dir / "chaos_insights.json"
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(parsed, f, indent=2)

                # Embed into model
                if "Agent_Insights" not in model_data:
                    model_data["Agent_Insights"] = {}
                model_data["Agent_Insights"]["Chaos"] = parsed

                with open(systems_model_path, "w", encoding="utf-8") as f:
                    json.dump(model_data, f, indent=2)

                st.success(f"✅ Chaos insights saved to: {output_path} and embedded in model.")
            except Exception as parse_err:
                st.warning("⚠️ Could not parse output. Please review raw response.")

        except Exception as e:
            st.error(f"OpenAI API error: {e}")
