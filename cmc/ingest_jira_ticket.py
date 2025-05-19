# ingest_jira_ticket.py
import json

def ingest(path: str) -> list:
    with open(path, "r") as f:
        raw_ticket = json.load(f)

    return [{
        "id": raw_ticket["ticket_id"],
        "type": "ticket",
        "initiator": raw_ticket["assignee"],
        "tool": "Jira",
        "related_to": raw_ticket.get("component"),
        "timestamp": raw_ticket.get("created"),
        "summary": raw_ticket["summary"]
    }]
