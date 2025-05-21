# run_pipeline.py
# CMC pipeline: dynamically build full systems_model.json using modular loaders

import json
from cmc.ingest.tools_loader import ToolsLoader
from cmc.ingest.applications_loader import ApplicationsLoader
from cmc.ingest.people_loader import PeopleLoader
from cmc.ingest.servers_loader import ServersLoader
from cmc.ingest.teams_loader import TeamsLoader
from cmc.ingest.events_loader import EventsLoader

OUTPUT_PATH = "data/systems_model.json"

def build_full_mental_model():
    model = {
        "tools": ToolsLoader().load(),
        "applications": ApplicationsLoader().load(),
        "people": PeopleLoader().load(),
        "servers": ServersLoader().load(),
        "teams": TeamsLoader().load(),
        "events": EventsLoader().load()
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(model, f, indent=2)

    print(f"✅ systems_model.json generated at {OUTPUT_PATH}")

if __name__ == "__main__":
    build_full_mental_model()
# run_pipeline.py
# CMC pipeline: dynamically build full systems_model.json using modular loaders

import json
from cmc.ingest.tools_loader import ToolsLoader
from cmc.ingest.applications_loader import ApplicationsLoader
from cmc.ingest.people_loader import PeopleLoader
from cmc.ingest.servers_loader import ServersLoader
from cmc.ingest.teams_loader import TeamsLoader
from cmc.ingest.events_loader import EventsLoader

OUTPUT_PATH = "data/systems_model.json"

def build_full_mental_model():
    model = {
        "tools": ToolsLoader().load(),
        "applications": ApplicationsLoader().load(),
        "people": PeopleLoader().load(),
        "servers": ServersLoader().load(),
        "teams": TeamsLoader().load(),
        "events": EventsLoader().load()
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(model, f, indent=2)

    print(f"✅ systems_model.json generated at {OUTPUT_PATH}")

if __name__ == "__main__":
    build_full_mental_model()
