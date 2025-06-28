import os
import requests
import json
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

    def fetch_commits(self) -> List[dict]:
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/commits"
        print("📡 Fetching commits from:", url)
        response = requests.get(url, headers=self.headers)

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
                    "name": f"COMMIT-{sha[:7]}",
                    "type": "commit",
                    "tool": "GitHub",
                    "initiator": author or "Unknown",
                    "related_to": message or "Unknown",
                    "timestamp": timestamp,
                    "tags": ["github", "commit"]
                },
                "llm_reasoning": "This object represents a GitHub commit event, including metadata like author, timestamp, and message. It’s a key aspect of Change Management and version control in IT organizations."
            }
            events.append(event)

        print(f"✅ Loaded {len(events)} commits")
        return events

    def fetch_pull_requests(self) -> List[dict]:
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/pulls?state=all&per_page=100"
        print("📡 Fetching pull requests from:", url)

        pr_events = []
        page = 1
        while True:
            paged_url = f"{url}&page={page}"
            response = requests.get(paged_url, headers=self.headers)
            if response.status_code != 200:
                print(f"❌ Failed to fetch pull requests: {response.status_code} {response.text}")
                break

            prs = response.json()
            if not prs:
                break  # End of pages

            for pr in prs:
                pr_event = {
                    "data": {
                        "id": f"PR-{pr['number']}",
                        "name": f"PR-{pr['number']}",
                        "type": "pull_request",
                        "tool": "GitHub",
                        "initiator": pr['user']['login'],
                        "related_to": pr['title'],
                        "timestamp": pr['created_at'],
                        "tags": ["github", "pull_request", pr['state']]
                    },
                    "llm_reasoning": "This object represents a GitHub pull request, including metadata like who opened it, when, and its title. Pull requests are formal code reviews and merge processes crucial to change control."
                }
                pr_events.append(pr_event)

            page += 1

        print(f"✅ Loaded {len(pr_events)} pull requests")
        return pr_events

    def load(self) -> List[dict]:
        if not self.token:
            print("❌ GitHub token not found in environment variable 'GITHUB_TOKEN'")
            return []

        commits = self.fetch_commits()
        pull_requests = self.fetch_pull_requests()

        all_events = commits + pull_requests
        print("🧪 Combined commit and PR events:")
        print(json.dumps(all_events, indent=2))

        return all_events
