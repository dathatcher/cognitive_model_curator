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

# 🔽 Project dropdown
project_dirs = sorted(glob("projects/*"))
if not project_dirs:
    st.error("⚠️ No projects found in 'projects/' folder.")
    st.stop()

project_name_map = {Path(p).name: p for p in project_dirs}
project_selection = st.selectbox("📂 Select a project:", list(project_name_map.keys()))
project_dir = project_name_map[project_selection]

# ❗ Validate project folder
if not Path(project_dir).exists():
    st.error("⚠️ Invalid project directory.")
    st.stop()

# ✅ Load system model
systems_model_path = Path(project_dir) / "systems_model.json"
if not systems_model_path.exists():
    st.error("⚠️ systems_model.json not found in that directory.")
    st.stop()

with open(systems_model_path, "r") as f:
    model_data = json.load(f)

distinctions = list(model_data.keys())

# ✅ Load CAS type from meta.json (if available)
cas_type = "the system"
meta_path = Path(project_dir) / "meta.json"
if meta_path.exists():
    try:
        with open(meta_path, "r") as f:
            meta_data = json.load(f)
            cas_type = meta_data.get("cas_type", "the system")
    except:
        pass

# 🧠 User Input
st.markdown(f"### 📄 Describe expectations, protocols, or behaviors in your **{cas_type}**:")
raw_text = st.text_area("Narrative text", height=250, placeholder="e.g., All changes must be approved by a team lead...")

if st.button("📏 Extract Rules with GPT-4"):
    with st.spinner("Analyzing..."):
        prompt = f"""
You are a systems thinking expert. A user has described patterns, policies, and rules within a {cas_type.lower()}.

Please extract both formal (e.g., written policy, technical requirement) and informal (e.g., cultural expectations, implicit behavior) **rules** from the following description.

For each rule:
- Give it a short, clear **name** (e.g., "MFA Requirement", "Curfew Policy")
- Write a 1-2 sentence **description**
- Suggest related distinctions from this list: {distinctions}

Output your response as a **strict JSON array**, like:
[
  {{
    "name": "...",
    "description": "...",
    "related_to": ["...", "..."]
  }}
]
Do not include explanations or extra text.

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
                    st.error("❌ Failed to parse LLM output. See below:")
                    st.code(content)
                    st.stop()

            for rule in extracted_rules:
                rule["cas_type"] = cas_type
                rule["distinction"] = "Rules"
                rule["source"] = "LLM Extraction"

            # ✅ Ensure Rules key exists
            if "Rules" not in model_data:
                model_data["Rules"] = []

            model_data["Rules"].extend(extracted_rules)

            with open(systems_model_path, "w") as f:
                json.dump(model_data, f, indent=2)

            st.success(f"Added {len(extracted_rules)} rule(s) to the mental model.")
        except Exception as e:
            st.error(f"OpenAI API error: {e}")
