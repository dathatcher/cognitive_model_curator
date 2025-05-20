# ingest_github_commit.py
import json
import re
from cmc.ai_utils import run_llm_prompt

def ingest(path: str) -> list:
    with open(path, "r") as f:
        raw_commit = json.load(f)

    message = raw_commit["message"]
    jira_match = re.search(r"JIRA-\d+", message)

    prompt = f"""
You are evaluating a GitHub commit message from a DevOps team.

### Context:
The organization has the following commit policy:
- Must include at least 10 words
- Must reference a Jira ticket (JIRA-####)
- Should describe both what changed and why

### Task:
Classify the following commit message:

\"\"\"{message}\"\"\"

### Output:
Respond ONLY with valid JSON:
{{
  "intention": "Positive" | "Neutral" | "Negative",
  "policy_violations": ["..."],
  "justification": "short explanation"
}}
"""

    response_text = run_llm_prompt(prompt)
    print("[LLM Response]", response_text)  # 🐞 Debugging

    try:
        parsed = json.loads(response_text)
    except Exception as e:
        print(f"[Parse Error] {e}")
        parsed = {
            "intention": "Neutral",
            "policy_violations": ["unparsable_llm_response"],
            "justification": "LLM response could not be parsed"
        }

    return [{
        "id": f"COMMIT-{raw_commit['commit_id']}",
        "type": "commit",
        "initiator": raw_commit["author"],
        "tool": "GitHub",
        "related_to": jira_match.group(0) if jira_match else None,
        "timestamp": raw_commit["timestamp"],
        "message": message,
        "intention": parsed["intention"],
        "policy_violations": parsed.get("policy_violations"),
        "justification": parsed.get("justification")
    }]
