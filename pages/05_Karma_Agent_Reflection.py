import streamlit as st
import json
from pathlib import Path
from openai import OpenAI
from glob import glob
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Karma Agent: Ethical Reflection", page_icon="🧘")
st.title("🧘 Karma Agent: Ethical Insight Generator")

# Select project folder
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

# Load distinctions
with open(systems_model_path, "r") as f:
    model_data = json.load(f)

all_distinctions = list(model_data.keys())
selected_distinctions = st.multiselect(
    "🧩 Select distinctions to reflect on ethically:",
    all_distinctions,
    default=["Roles", "Rules"]
)

# Prepare filtered data for LLM
filtered_data = {k: v for k, v in model_data.items() if k in selected_distinctions}

if st.button("🌱 Generate Ethical Insights"):
    with st.spinner("Reflecting ethically..."):
        prompt = f"""
You are the Karma Agent. Reflect on the ethical, emotional, and moral dynamics within this complex adaptive system (CAS). The user has selected the following distinctions to analyze:

Distinctions: {selected_distinctions}

Data:
{json.dumps(filtered_data, indent=2)}

For each insight:
- Describe the **ethical or moral concern**
- Indicate **risk level** (low, moderate, high)
- List affected **roles**
- Reference any relevant **rules**

Return a JSON array like:
[
  {{
    "insight": "...",
    "risk_level": "moderate",
    "affected_roles": ["..."],
    "referenced_rules": ["..."]
  }}
]
Do not include explanations or markdown.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are an ethical reflection engine (Karma Agent)."},
                    {"role": "user", "content": prompt}
                ]
            )
            insights = response.choices[0].message.content.strip()
            st.markdown("### 🪞 Karma Insights")
            st.code(insights, language="json")

            try:
                parsed = json.loads(insights)

                # Save to karma_insights.json
                insights_path = project_dir / "karma_insights.json"
                with open(insights_path, "w") as f:
                    json.dump(parsed, f, indent=2)
                st.success(f"Saved to {insights_path}")

                # Also embed in systems_model.json
                if "Agent_Insights" not in model_data:
                    model_data["Agent_Insights"] = {}

                model_data["Agent_Insights"]["Karma"] = parsed

                with open(systems_model_path, "w") as f:
                    json.dump(model_data, f, indent=2)
                st.success("Embedded Karma insights into systems_model.json ✅")

            except Exception as parse_err:
                st.warning("⚠️ Could not parse JSON. Showing raw response instead.")

        except Exception as e:
            st.error(f"OpenAI API error: {e}")
