# ingest_github_commit.py
import json
import re

def ingest(path: str) -> list:
    with open(path, "r") as f:
        raw_commit = json.load(f)

    jira_match = re.search(r"JIRA-\d+", raw_commit["message"])
    return [{
        "id": f"COMMIT-{raw_commit['commit_id']}",
        "type": "commit",
        "initiator": raw_commit["author"],
        "tool": "GitHub",
        "related_to": jira_match.group(0) if jira_match else None,
        "timestamp": raw_commit["timestamp"],
        "message": raw_commit["message"]
    }]
