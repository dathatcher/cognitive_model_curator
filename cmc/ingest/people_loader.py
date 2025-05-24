class PeopleLoader:
    def __init__(self, source_data=None):
        self.source = source_data

    def load(self) -> list:
        return [
            {
                "name": "Jane Doe",
                "role": "Site Reliability Engineer",
                "teams": ["SRE", "DevOps"],
                "uses_tools": ["Terraform", "Datadog", "Jira"]
            },
            {
                "name": "DA Thatcher",
                "role": "Compliance Repetitive",
                "teams": [],
                "uses_tools": []
            }
        ]
