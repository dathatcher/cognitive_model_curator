import json
from cmc.ingest.tools_loader import ToolsLoader
from cmc.ingest.applications_loader import ApplicationsLoader
from cmc.ingest.people_loader import PeopleLoader
from cmc.ingest.servers_loader import ServersLoader
from cmc.ingest.teams_loader import TeamsLoader
from cmc.ingest.events_loader import EventsLoader
from cmc.ingest.networks_loader import NetworksLoader

def build_mental_model():
    model = {
        "tools": ToolsLoader().load(),
        "applications": ApplicationsLoader().load(),
        "people": PeopleLoader().load(),
        "servers": ServersLoader().load(),
        "networks": NetworksLoader().load(),
        "teams": TeamsLoader().load(),
        "events": EventsLoader().load()
    }

    with open("../output/systems_model.json", "w") as f:
        json.dump(model, f, indent=2)
    print("✅ systems_model.json generated.")

if __name__ == "__main__":
    build_mental_model()
