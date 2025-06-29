import json
from cmc.ingest.tools_loader import ToolsLoader
from cmc.ingest.applications_loader import ApplicationsLoader
from cmc.ingest.people_loader import PeopleLoader
from cmc.ingest.servers_loader import ServersLoader
from cmc.ingest.teams_loader import TeamsLoader
from cmc.ingest.networks_loader import NetworksLoader
from cmc.ingest.github_loader import GitHubLoader  # ✅ NEW IMPORT (for GitHub events)
# from cmc.ingest.events_loader import EventsLoader  # (Removed: legacy EventsLoader no longer needed)

def build_mental_model():
    # Load data from standard loaders into the system model
    model = {
        "tools": ToolsLoader().load(),
        "applications": ApplicationsLoader().load(),
        "people": PeopleLoader().load(),
        "servers": ServersLoader().load(),
        "networks": NetworksLoader().load(),
        "teams": TeamsLoader().load(),
        "Change Management": []  # ✅ NEW: Initialize Change Management list for PR events
    }

    # Load GitHub events (e.g., PR commits) from the specified repository
    github_loader = GitHubLoader(repo_owner="dathatcher", repo_name="wisdom-test-app")
    github_events = github_loader.load()

    # Merge GitHub events into the Change Management list
    model["Change Management"].extend(github_events)

    # Output the full system model to JSON
    with open("../output/systems_model.json", "w") as f:
        json.dump(model, f, indent=2)

    print("✅ systems_model.json generated with GitHub commits included.")

if __name__ == "__main__":
    build_mental_model()
