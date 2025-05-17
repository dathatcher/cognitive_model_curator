# ingest_github_commit.py
# Reads a raw commit file and updates mental_model.json with a Wisdom Layer event

import json
import os
import re

RAW_COMMIT_PATH = os.path.join("..", "data", "input_events", "commit_123.json")
MENTAL_MODEL_PATH = os.path.join("..", "data", "mental_model.json")

def load_raw_commit(path):
    with open(path, "r") as f:
        return json.load(f)

def parse_commit_event(raw_commit):
    jira_match = re.search(r"JIRA-\d+", raw_commit["message"])
    return {
        "id": f"COMMIT-{raw_commit['commit_id']}",
        "type": "commit",
        "initiator": raw_commit["author"],
        "tool": "GitHub",
        "related_to": jira_match.group(0) if jira_match else None,
        "timestamp": raw_commit["timestamp"],
        "message": raw_commit["message"]
    }

def load_mental_model(path):
    if not os.path.exists(path):
        return {"events": []}
    with open(path, "r") as f:
        return json.load(f)

def save_mental_model(path, model):
    with open(path, "w") as f:
        json.dump(model, f, indent=2)

if __name__ == "__main__":
    raw_commit = load_raw_commit(RAW_COMMIT_PATH)
    event = parse_commit_event(raw_commit)

    model = load_mental_model(MENTAL_MODEL_PATH)
    model.setdefault("events", [])

    if event["id"] not in [e["id"] for e in model["events"]]:
        model["events"].append(event)
        save_mental_model(MENTAL_MODEL_PATH, model)
        print(f"✅ Event {event['id']} added to mental_model.json")
    else:
        print(f"⚠️ Event {event['id']} already exists")

    print(json.dumps(event, indent=2))
