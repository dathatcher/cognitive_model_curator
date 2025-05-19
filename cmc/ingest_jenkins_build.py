# ingest_jenkins_build.py
import json
import re

def ingest(path: str) -> list:
    with open(path, "r") as f:
        raw = json.load(f)

    related = []

    if "related_event_id" in raw:
        related.append(raw["related_event_id"])
    elif "related_event_ids" in raw and isinstance(raw["related_event_ids"], list):
        related.extend(raw["related_event_ids"])

    if not related:
        commit_matches = re.findall(r"[a-f0-9]{6,10}", raw.get("release_tag", ""))
        jira_matches = re.findall(r"JIRA-\d+", raw.get("release_tag", ""))
        related.extend([f"COMMIT-{m}" for m in commit_matches])
        related.extend(jira_matches)

    return [{
        "id": f"JENKINS-{raw['build_id']}",
        "type": "deployment",
        "initiator": raw.get("triggered_by", "CI Pipeline"),
        "tool": "Jenkins",
        "related_to": related if related else None,
        "timestamp": raw.get("timestamp"),
        "summary": f"Deployed version {raw.get('release_tag')} to {raw.get('environment')}"
    }]
