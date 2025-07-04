import streamlit as st
import json
import os
from utils.model_loader import load_model, save_model
from utils.llm_interface import call_llm_for_suggestions

st.set_page_config(page_title="LLM-Powered Model Editor", layout="wide")
st.title("🧠 LLM-Powered Model Editor")

MODEL_PATH = "data/systems_model.json"
model = load_model(MODEL_PATH)

project = st.selectbox("📂 Select a project:", [model.get("project_id", "unknown")])
distinctions = [k for k in model.keys() if isinstance(model[k], list)]
selected_distinction = st.selectbox("🎯 Select distinction to update:", distinctions)

st.markdown("💬 Ask the LLM to add or revise elements")
prompt = st.text_area("e.g., Add institutions that support democratic processes or recommend oversight systems")

if st.button("Ask LLM"):
    with st.spinner("Thinking..."):
        llm_response = call_llm_for_suggestions(prompt, context=selected_distinction)
        try:
            proposed_json = json.loads(llm_response)
            st.success("✨ Proposed Additions/Changes")
            st.json(proposed_json)

            if st.button("✅ Add to systems_model.json"):
                model[selected_distinction].extend(proposed_json)
                save_model(model, MODEL_PATH)
                st.success("Added to model and saved successfully.")
        except json.JSONDecodeError:
            st.error("❌ Could not parse LLM response as valid JSON.")
            st.code(llm_response)
