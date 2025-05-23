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

# System role classification using Systems Thinking
def classify_role(data):
    if any(k in data for k in ["hostname", "vlan_name", "subnet", "IP Address"]):
        return "input"
    elif any(k in data for k in ["runs", "deployed_on", "owns_apps"]):
        return "transform"
    elif any(k in data for k in ["responds_to"]):
        return "feedback"
    elif any(k in data for k in ["uses_tools", "monitors_apps"]):
        return "feedback"
    elif any(k in data for k in ["monitored_by"]):
        return "output"
    return "context"

role_levels = {"input": 0, "transform": 1, "output": 2, "feedback": 3, "context": 4}

# Initialize graph
G = nx.DiGraph()
category_colors = {
    "Infrastructure": "#1f77b4",
    "Applications": "#2ca02c",
    "Human Interactions": "#ff7f0e",
    "Change Management": "#9467bd",
    "Incident Response": "#d62728"
}

node_roles = {}

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
        system_role = classify_role(data)
        node_roles[node_id] = system_role

        G.add_node(node_id, label=node_id, node_color=node_color, role=system_role)

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

# Layout by system role level
def layered_layout(G, role_levels):
    pos = {}
    layer_x = {}
    spacing_x = 2
    spacing_y = -2
    for node, data in G.nodes(data=True):
        role = data.get("role", "context")
        layer = role_levels.get(role, 4)
        x = layer_x.get(layer, 0)
        pos[node] = (x, spacing_y * layer)
        layer_x[layer] = x + spacing_x
    return pos

pos = layered_layout(G, role_levels)
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
