# run_pipeline.py
# Cognitive Model Curator end-to-end runner

import json
from cmc.ingest_github_commit import ingest as ingest_github
from cmc.ingest_jira_ticket import ingest as ingest_jira
from cmc.ingest_jenkins_build import ingest as ingest_jenkins
from cmc.orchestrator import orchestrate

MENTAL_MODEL_PATH = "data/mental_model.json"

# Load or initialize mental model
try:
    with open(MENTAL_MODEL_PATH, "r") as f:
        model = json.load(f)
except FileNotFoundError:
    model = {"events": []}

# Run ingestion modules
print("[Ingest] GitHub...")
events_github = ingest_github("data/input_events/commit_123.json")
print("[Ingest] Jira...")
events_jira = ingest_jira("data/input_events/jira_123.json")
print("[Ingest] Jenkins...")
events_jenkins = ingest_jenkins("data/input_events/jenkins_049.json")

# Merge into mental model
model["events"].extend(events_github + events_jira + events_jenkins)

# Run orchestration
print("[Orchestrate] Tagging and sorting events...")
model["events"] = orchestrate(model["events"], verbose=True)

# Save output
with open(MENTAL_MODEL_PATH, "w") as f:
    json.dump(model, f, indent=2)

print("✅ Updated mental_model.json with orchestrated events.")