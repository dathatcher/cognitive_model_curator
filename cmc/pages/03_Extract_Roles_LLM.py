import streamlit as st
import json
import ast
from pathlib import Path
import os
from glob import glob
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Extract Rules from Text", page_icon="📏")
st.title("📏 LLM-Powered Rule Extraction")

# 🔍 Auto-detect latest project directory
def get_latest_project_path():
    project_dirs = sorted(glob("cmc/data/*"), key=os.path.getmtime, reverse=True)
    return project_dirs[0] if project_dirs else ""

auto_path = get_latest_project_path()
project_dir = st.text_input("📁 Project folder path:", value=auto_path)

# ❗Validation
if not project_dir or not Path(project_dir).exists():
    st.error("⚠️ Could not find a valid project directory. Make sure one has been initialized.")
    st.stop()

systems_model_path = Path(project_dir) / "systems_model.json"
if not systems_model_path.exists():
    st.error("⚠️ systems_model.json not found in that directory.")
    st.stop()

# ✅ Load the mental model
with open(systems_model_path, "r") as f:
    model_data = json.load(f)

distinctions = list(model_data.keys())

st.markdown("### 📄 Paste a description of household expectations, discipline, or structure:")
raw_text = st.text_area("Narrative text", height=250, placeholder="e.g., Children must do homework before screen time. The daughter must be home by 10pm...")

if st.button("📏 Extract Rules with GPT-4"):
    with st.spinner("Analyzing..."):
        prompt = f"""
You are a systems thinking expert. A user has described patterns of discipline and expectations within a family system.

Please extract the **rules** from the text — including both explicit rules (e.g., curfew, screen time) and implicit ones (e.g., emotional tone, who makes decisions).

For each rule:
- Assign a clear **name** (e.g., "Curfew Policy")
- Provide a **description** of how it functions or what it implies
- Suggest related distinctions (choose from: {distinctions})

Return your response as a **strict JSON array** with the following format:
[
  {{
    "name": "...",
    "description": "...",
    "related_to": ["...", "..."]
  }}
]
Do not include any text or explanation. Only output valid JSON.

Text:
\"\"\"{raw_text}\"\"\"
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a cognitive systems modeler."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content.strip()
            st.markdown("### ✅ Extracted Rules")
            st.code(content, language="json")

            try:
                extracted_rules = json.loads(content)
            except json.JSONDecodeError:
                try:
                    extracted_rules = ast.literal_eval(content)
                except Exception as eval_err:
                    st.error("❌ Still failed to parse LLM output. See below:")
                    st.code(content)
                    st.stop()

            for rule in extracted_rules:
                rule["cas_type"] = "Family Structure"
                rule["distinction"] = "Rules"
                rule["source"] = "LLM Extraction"

            model_data["Rules"].extend(extracted_rules)

            with open(systems_model_path, "w") as f:
                json.dump(model_data, f, indent=2)

            st.success(f"Added {len(extracted_rules)} rule(s) to the mental model.")
        except Exception as e:
            st.error(f"OpenAI API error: {e}")
