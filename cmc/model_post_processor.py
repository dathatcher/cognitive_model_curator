import os
import json
from datetime import datetime
from pathlib import Path

class MentalModelPostProcessor:
    def __init__(self, input_path="data/systems_model.json", output_dir="models"):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.model = self._load_model()

    def _load_model(self):
        if not self.input_path.exists():
            raise FileNotFoundError(f"Mental model not found at {self.input_path}")
        with open(self.input_path) as f:
            return json.load(f)

    def _infer_relationships(self):
        relationships = []
        apps_by_name = {}
        hosts_by_name = {}
        tools_by_name = {}
        teams_by_name = {}
        people_by_name = {}
        prs_by_name = {}

        # Index relevant items
        for category, entries in self.model.items():
            if not isinstance(entries, list):
                continue
            for entry in entries:
                data = entry.get("data", {})
                if "name" in data:
                    if category == "Applications":
                        apps_by_name[data["name"]] = data
                    elif category == "Human Interactions":
                        people_by_name[data["name"]] = data
                    elif category in ["Infrastructure", "Change Management"]:
                        tools_by_name[data["name"]] = data
                    elif category == "Teams":
                        teams_by_name[data["name"]] = data
                    elif data["name"].startswith("PR-"):
                        prs_by_name[data["name"]] = data
                if "hostname" in data:
                    hosts_by_name[data["hostname"]] = data

        # Build relationships
        for category, entries in self.model.items():
            if not isinstance(entries, list):
                continue
            for entry in entries:
                data = entry.get("data", {})

                if "runs" in data:
                    for app in data["runs"]:
                        relationships.append({
                            "type": "runs",
                            "source": data.get("hostname", "unknown_host"),
                            "target": app
                        })

                if "deployed_on" in data:
                    for host in data["deployed_on"]:
                        relationships.append({
                            "type": "deployed_on",
                            "source": data.get("name", "unknown_app"),
                            "target": host
                        })

                if "owned_by" in data:
                    relationships.append({
                        "type": "owns",
                        "source": data["owned_by"],
                        "target": data.get("name", "unknown_entity")
                    })

                if "monitored_by" in data:
                    for monitor in data["monitored_by"]:
                        relationships.append({
                            "type": "monitors",
                            "source": monitor,
                            "target": data.get("name", "unknown_monitored")
                        })

                if "uses_tools" in data:
                    for tool in data["uses_tools"]:
                        relationships.append({
                            "type": "uses_tool",
                            "source": data.get("name", "unknown_person"),
                            "target": tool
                        })

                if data.get("type") == "workflow_run":
                    workflow_id = data.get("id")
                    related_to = data.get("related_to")
                    for pr_name in prs_by_name:
                        if related_to == prs_by_name[pr_name].get("related_to"):
                            relationships.append({
                                "type": "deploys",
                                "source": workflow_id,
                                "target": prs_by_name[pr_name]["id"]
                            })

        return relationships

    def post_process_and_save(self):
        self.model["relationships"] = self._infer_relationships()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        output_path = self.output_dir / f"systems_model_{timestamp}.json"
        with open(output_path, "w") as f:
            json.dump(self.model, f, indent=2)

        with open(self.input_path, "w") as f:
            json.dump(self.model, f, indent=2)

        return output_path
