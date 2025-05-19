# orchestrator.py
# Wisdom Layer Event Orchestration Prototype

import hashlib
from datetime import datetime

def deduplicate(events, verbose=False):
    """Remove exact duplicates by event ID"""
    seen = set()
    deduped = []
    for e in events:
        if e["id"] not in seen:
            deduped.append(e)
            seen.add(e["id"])
        elif verbose:
            print(f"[deduplicate] Removed duplicate event: {e['id']}")
    return deduped

def infer_phase(event_type):
    if "jira" in event_type.lower() or event_type.lower() == "ticket":
        return "plan"
    elif "commit" in event_type.lower():
        return "build"
    elif "deploy" in event_type.lower() or event_type.lower() == "deployment":
        return "release"
    else:
        return "unknown"

def assign_event_group(event):
    base = event.get("related_to") or event.get("id")
    if isinstance(base, list):
        base = "-".join(sorted(base))
    tag = base or event.get("id") or "ungrouped"
    return f"group-{hashlib.md5(tag.encode()).hexdigest()[:6]}"

def orchestrate(events, verbose=False):
    orchestrated = []
    deduped = deduplicate(events, verbose=verbose)

    for e in deduped:
        e = e.copy()
        e["phase"] = infer_phase(e.get("type", ""))
        e["event_group"] = assign_event_group(e)

        if verbose:
            print(f"[orchestrate] {e['id']} → phase: {e['phase']} → group: {e['event_group']}")

        # Ensure timestamp is sortable
        try:
            e["_ts"] = datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00"))
        except:
            e["_ts"] = datetime.now()

        orchestrated.append(e)

    orchestrated.sort(key=lambda x: x["_ts"])
    for e in orchestrated:
        del e["_ts"]

    return orchestrated
