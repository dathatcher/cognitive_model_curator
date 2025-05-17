# ingest_jenkins_build.py
# Reads a raw Jenkins build event and updates mental_model.json with a Wisdom Layer event

import json
import os

RAW_JENKINS_PATH = os.path.join("..", "data", "input_events", "jenkins_049.json")
MENTAL_MODEL_PATH = os.path.join("..", "data", "mental_model.json")

def load_raw_jenkins(path):
    with open(path, "r") as f:
        return json.load(f)

def parse_jenkins_event(raw):
    return {
        "id": f"JENKINS-{raw['build_id']}",
        "type": "deployment",
        "initiator": raw.get("triggered_by", "CI Pipeline"),
        "tool": "Jenkins",
        "related_to": raw.get("application"),
        "timestamp": raw.get("timestamp"),
        "summary": f"Deployed version {raw.get('release_tag')} to {raw.get('environment')}"
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
    raw_build = load_raw_jenkins(RAW_JENKINS_PATH)
    event = parse_jenkins_event(raw_build)

    model = load_mental_model(MENTAL_MODEL_PATH)
    model.setdefault("events", [])

    if event["id"] not in [e["id"] for e in model["events"]]:
        model["events"].append(event)
        save_mental_model(MENTAL_MODEL_PATH, model)
        print(f"✅ Event {event['id']} added to mental_model.json")
    else:
        print(f"⚠️ Event {event['id']} already exists")

    print(json.dumps(event, indent=2))
