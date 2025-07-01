### ✅ Updated GitHubLoader with commit, PR, and workflow run support
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
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/pulls?state=all"
        print("📡 Fetching pull requests from:", url)
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"❌ Failed to fetch pull requests: {response.status_code} {response.text}")
            return []

        prs = response.json()
        pr_events = []

        for pr in prs:
            pr_number = pr["number"]
            pr_title = pr["title"]
            pr_commits_url = pr["commits_url"]
            pr_source_branch = pr["head"]["ref"]
            pr_state = pr["state"]

            pr_commit_resp = requests.get(pr_commits_url, headers=self.headers)
            pr_commit_shas = []
            if pr_commit_resp.status_code == 200:
                pr_commit_data = pr_commit_resp.json()
                pr_commit_shas = [f"COMMIT-{c['sha'][:7]}" for c in pr_commit_data]

            pr_event = {
                "data": {
                    "id": f"PR-{pr_number}",
                    "name": f"PR-{pr_number}",
                    "type": "pull_request",
                    "tool": "GitHub",
                    "initiator": pr["user"]["login"],
                    "related_to": pr_source_branch,
                    "timestamp": pr["created_at"],
                    "tags": ["github", "pull_request", pr_state],
                    "sub_events": pr_commit_shas,
                    "_force_class": "Change Management"
                },
                "llm_reasoning": (
                    "This object represents a GitHub pull request with linked commit SHAs. "
                    "It captures metadata like the source branch, associated commits, and initiator. "
                    "This traceability is essential for enforcing policy and tracking change control."
                )
            }
            pr_events.append(pr_event)

        print(f"✅ Loaded {len(pr_events)} pull requests with linked commits")
        return pr_events

    def fetch_workflow_runs(self) -> List[dict]:
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/runs"
        print("📡 Fetching GitHub Actions workflow runs from:", url)
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"❌ Failed to fetch workflow runs: {response.status_code} {response.text}")
            return []

        runs = response.json().get("workflow_runs", [])
        workflow_events = []

        for run in runs:
            event = {
                "data": {
                    "id": f"ACTION-{run['id']}",
                    "name": run.get("name") or f"Workflow-{run['id']}",
                    "type": "workflow_run",
                    "tool": "GitHub Actions",
                    "initiator": run.get("actor", {}).get("login", "Unknown"),
                    "related_to": run.get("head_branch", "unknown-branch"),
                    "timestamp": run.get("created_at"),
                    "tags": [
                        "github", "actions", run.get("status", "unknown"), run.get("conclusion", "unknown")
                    ],
                    "_force_class": "Change Management"
                },
                "llm_reasoning": (
                    "This object represents a GitHub Actions workflow run. It includes metadata like status, "
                    "conclusion, actor, and related PR branch. These automated deployments are part of formal change "
                    "control and CI/CD processes in IT organizations."
                )
            }
            workflow_events.append(event)

        print(f"✅ Loaded {len(workflow_events)} workflow runs")
        return workflow_events

    def load(self) -> List[dict]:
        if not self.token:
            print("❌ GitHub token not found in environment variable 'GITHUB_TOKEN'")
            return []

        commits = self.fetch_commits()
        pull_requests = self.fetch_pull_requests()
        workflows = self.fetch_workflow_runs()

        all_events = commits + pull_requests + workflows
        print("🧪 Combined commit, PR, and Actions events:")
        print(json.dumps(all_events, indent=2))

        return all_events
