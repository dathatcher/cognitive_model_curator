import streamlit as st
import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the system model
st.set_page_config(page_title="Wisdom Layer IT Model Viewer", layout="wide")
st.title("🧠 Wisdom Layer IT Organization Model")

uploaded_file = st.file_uploader("Upload your systems_model.json", type="json")
if not uploaded_file:
    st.warning("Please upload a systems_model.json file.")
    st.stop()

system_model = json.load(uploaded_file)

# Top-level filter selection
categories = [k for k in system_model.keys() if k not in ["NOT_DEFINED", "relationships", "Data Streams", "Security Protocols", "External Interfaces", "Regulatory Compliance"]]
selected_categories = st.multiselect("Select categories to display", categories, default=categories)

# Edge type filter selection
edge_types = set(rel["type"] for rel in system_model.get("relationships", []))
selected_edge_types = st.multiselect("Select edge types to display", sorted(edge_types), default=list(edge_types))

# Initialize graph
G = nx.DiGraph()
category_colors = {
    "Infrastructure": "#1f77b4",
    "Applications": "#2ca02c",
    "Human Interactions": "#ff7f0e",
    "Change Management": "#9467bd",
    "Incident Response": "#d62728"
}

# Extract nodes and edges
for category in selected_categories:
    for item in system_model.get(category, []):
        data = item.get("data", {})
        if not data:
            continue

        node_id = data.get("name") or data.get("hostname") or data.get("id")
        if not node_id:
            continue

        node_color = category_colors.get(category, "gray")
        G.add_node(node_id, label=node_id, node_color=node_color)

        if category == "Applications" and "relationships" in data:
            for rel_type, targets in data["relationships"].items():
                for target in targets:
                    if rel_type in selected_edge_types:
                        G.add_edge(node_id, target, label=rel_type)

        if category == "Infrastructure" and "runs" in data:
            for target in data["runs"]:
                if "runs" in selected_edge_types:
                    G.add_edge(node_id, target, label="runs")

        if category == "Change Management" and "related_to" in data:
            targets = data["related_to"] if isinstance(data["related_to"], list) else [data["related_to"]]
            for target in targets:
                if "related_to" in selected_edge_types:
                    G.add_edge(node_id, target, label="related_to")

        if category == "Human Interactions" and "uses_tools" in data:
            for tool in data["uses_tools"]:
                if "uses_tool" in selected_edge_types:
                    G.add_edge(node_id, tool, label="uses_tool")

# Add edges from the global relationships list
for rel in system_model.get("relationships", []):
    if rel["type"] in selected_edge_types:
        G.add_edge(rel["source"], rel["target"], label=rel["type"])

# Draw graph
pos = nx.spring_layout(G, k=0.8)
fig, ax = plt.subplots(figsize=(14, 10))
colors = [G.nodes[n].get("node_color", "gray") for n in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=colors, ax=ax, edge_color="#cccccc")

# Edge labels
edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True) if "label" in d}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=8)

st.pyplot(fig)

# Optional: Display node data
with st.expander("📘 View All Node Details"):
    for category, items in system_model.items():
        if not items or category not in selected_categories:
            continue
        st.subheader(category)
        for item in items:
            st.json(item)
