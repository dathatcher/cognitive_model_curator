
import streamlit as st
import openai
import os
import json
import re
from pathlib import Path
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Initialize Wisdom Layer Project", page_icon="🧠")
st.title("🧠 Wisdom Layer Project Initialization")

st.markdown("Start by defining the system you'd like to explore using Systems Thinking, Chaos Theory, Karma, and Complexity Sentinel agents.")

# Input from user
system_name = st.text_input("🌐 What is the name of the system?", placeholder="e.g., IT Organization, U.S. Democracy")
system_purpose = st.text_area("🎯 What is your purpose or intent in modeling this system?", height=100, placeholder="e.g., To understand fragility and feedback loops in our public institutions.")

if st.button("Generate Initial Mental Model"):
    if not system_name or not system_purpose:
        st.warning("Please fill out both fields to continue.")
        st.stop()

    with st.spinner("Calling GPT-4 Turbo to generate system distinctions..."):
        prompt = f"""You are an expert in systems thinking, chaos theory, and cognitive architecture. A user is modeling a complex system with agentic AI (using Systems Thinking, Chaos Theory, Karma, and Complexity Sentinel agents).

System Name: {system_name}
Purpose: {system_purpose}

Please propose an initial set of top-level distinctions (categories of entities) relevant to this system, and a brief metadata block that includes the system name, purpose, and potential blind spots or boundary concerns. Return a JSON object with two keys: 'top_level_distinctions' and 'meta'."""

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a cognitive systems architect."},
                    {"role": "user", "content": prompt}
                ]
            )
            result_text = response.choices[0].message.content.strip()
            st.success("Initial model generated.")
            st.code(result_text, language="json")

            # Extract the JSON portion using regex
            json_match = re.search(r"```json\n(.*?)```", result_text, re.DOTALL)
            if json_match:
                raw_json = json_match.group(1).strip()
            else:
                raw_json = result_text  # fallback if no code block

            try:
                result_json = json.loads(raw_json)
                distinctions_obj = result_json.get("top_level_distinctions", {})
                if isinstance(distinctions_obj, dict):
                    top_level_distinctions = list(distinctions_obj.keys())
                else:
                    top_level_distinctions = distinctions_obj

                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                project_slug = system_name.lower().replace(" ", "_")
                project_path = Path(f"cmc/data/{project_slug}_{timestamp}")
                project_path.mkdir(parents=True, exist_ok=True)

                # Write systems_model.json
                base_model = {key: [] for key in top_level_distinctions}
                with open(project_path / "systems_model.json", "w") as f:
                    json.dump(base_model, f, indent=2)

                # Write meta.json
                with open(project_path / "meta.json", "w") as f:
                    json.dump(result_json.get("meta", {}), f, indent=2)

                # Write raw LLM response for audit
                with open(project_path / "llm_response.txt", "w") as f:
                    f.write(result_text)

                st.success(f"📁 Project initialized at: {project_path}")

            except Exception as parse_err:
                st.error(f"Failed to parse LLM response: {parse_err}")
        except Exception as e:
            st.error(f"OpenAI API error: {e}")
