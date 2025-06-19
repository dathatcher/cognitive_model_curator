import os
import requests
from typing import List

class GitHubLoader:
    def __init__(self, repo_owner: str = "your-org-or-username", repo_name: str = "your-repo-name"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def load(self) -> List[dict]:
        if not self.token:
            print("❌ GitHub token not found in environment variable 'GITHUB_TOKEN'")
            return []

        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/commits"
        print("📡 Final URL:", url)
        print("📦 Headers used:")
        for k, v in self.headers.items():
            print(f"  {k}: {v[:10]}..." if k == "Authorization" else f"  {k}: {v}")

        response = requests.get(url, headers=self.headers)
        print("🔁 Status Code:", response.status_code)
        print("🔎 Response Text (start):", response.text[:200])

        if response.status_code != 200:
            print(f"❌ Failed to fetch commits: {response.status_code} {response.reason}")
            return []

        commits = response.json()
        events = []
        for commit in commits:
            sha = commit.get("sha")
            message = commit.get("commit", {}).get("message")
            author = commit.get("commit", {}).get("author", {}).get("name")
            timestamp = commit.get("commit", {}).get("author", {}).get("date")

            event = {
                "data": {
                    "id": f"COMMIT-{sha[:7]}",
                    "type": "commit",
                    "tool": "GitHub",
                    "initiator": author or "Unknown",
                    "related_to": "Unknown",
                    "timestamp": timestamp,
                    "tags": ["github", "commit"]
                },
                "llm_reasoning": "This data object represents a GitHub commit event captured via the GitHub API, containing essential metadata such as author, timestamp, and repository source, and is relevant to Change Management activities within an IT organization."
            }
            events.append(event)

        print(f"✅ Loaded {len(events)} commits from GitHub repo '{self.repo_owner}/{self.repo_name}'")
        return events
