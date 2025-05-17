# ingest_jira_ticket.py
# Reads a raw JIRA ticket and updates mental_model.json with a Wisdom Layer event

import json
import os

RAW_JIRA_PATH = os.path.join("..", "data", "input_events", "jira_123.json")
MENTAL_MODEL_PATH = os.path.join("..", "data", "mental_model.json")

def load_raw_jira(path):
    with open(path, "r") as f:
        return json.load(f)

def parse_jira_event(raw_ticket):
    return {
        "id": raw_ticket["ticket_id"],
        "type": "ticket",
        "initiator": raw_ticket["assignee"],
        "tool": "Jira",
        "related_to": raw_ticket.get("component"),
        "timestamp": raw_ticket.get("created"),
        "summary": raw_ticket["summary"]
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
    raw_ticket = load_raw_jira(RAW_JIRA_PATH)
    event = parse_jira_event(raw_ticket)

    model = load_mental_model(MENTAL_MODEL_PATH)
    model.setdefault("events", [])

    if event["id"] not in [e["id"] for e in model["events"]]:
        model["events"].append(event)
        save_mental_model(MENTAL_MODEL_PATH, model)
        print(f"✅ Event {event['id']} added to mental_model.json")
    else:
        print(f"⚠️ Event {event['id']} already exists")

    print(json.dumps(event, indent=2))
