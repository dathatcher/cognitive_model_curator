import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Add Roles to Mental Model", page_icon="➕")
st.title("➕ Add to Mental Model: Roles")

project_dir = st.text_input("📁 Enter project folder path (e.g., cmc/data/thatcher_family_20250702_012052):")

if project_dir:
    systems_model_path = Path(project_dir) / "systems_model.json"
    if systems_model_path.exists():
        with open(systems_model_path, "r") as f:
            model_data = json.load(f)

        st.subheader("📌 Add a Role to the Mental Model")
        role_name = st.text_input("🧍 Role name", placeholder="e.g., Mother, Child, Stepfather")
        role_description = st.text_area("📖 Description", placeholder="Describe this role's function or influence.")
        role_relationships = st.multiselect("🔗 Related Distinctions", model_data.keys(), default=[])

        if st.button("✅ Add Role"):
            if not role_name:
                st.warning("Role name is required.")
                st.stop()

            role_obj = {
                "name": role_name,
                "description": role_description,
                "related_to": role_relationships,
                "cas_type": "Family Structure",
                "distinction": "Roles",
                "source": "Manual Entry"
            }

            model_data["Roles"].append(role_obj)

            with open(systems_model_path, "w") as f:
                json.dump(model_data, f, indent=2)

            st.success(f"Added role: {role_name}")
            st.json(role_obj)
    else:
        st.error("Could not find systems_model.json in the specified directory.")
