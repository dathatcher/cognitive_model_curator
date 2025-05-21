class TeamsLoader:
    def __init__(self, source_data=None):
        self.source = source_data

    def load(self) -> list:
        return [
            {
                "name": "DevOps",
                "roles": ["Site Reliability Engineer", "Platform Engineer"],
                "members": ["Jane Doe"],
                "responsibilities": {
                    "owns_tools": ["Terraform", "Jira"],
                    "monitors_apps": ["PayrollApp"],
                    "integrates_with": ["Slack"]
                }
            },
            {
                "name": "Observability",
                "roles": ["Monitoring Engineer"],
                "members": [],
                "responsibilities": {
                    "owns_tools": ["Datadog"],
                    "monitors_apps": [],
                    "integrates_with": []
                }
            },
            {
                "name": "SRE",
                "roles": ["Site Reliability Engineer"],
                "members": ["Jane Doe"],
                "responsibilities": {
                    "responds_to": ["PayrollApp"],
                    "uses_tools": ["Datadog", "Terraform"]
                }
            },
            {
                "name": "HR Dev Team",
                "roles": ["Application Developer"],
                "members": [],
                "responsibilities": {
                    "owns_apps": ["PayrollApp"]
                }
            }
        ]
