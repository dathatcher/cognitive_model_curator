class ToolsLoader:
    def __init__(self, source_data=None):
        self.source = source_data

    def load(self) -> list:
        return [
            {
                "name": "Datadog",
                "type": "Observability",
                "relationships": {
                    "monitors_applications": ["PayrollApp", "BillingService"],
                    "used_by_teams": ["Observability", "DevOps"],
                    "integrates_with": ["Jira", "Slack"]
                },
                "systems": ["MonitoringStack"],
                "perspectives": {
                    "ObservabilityTeam": "Essential APM",
                    "DevOpsTeam": "Optional/experimental",
                    "SecurityTeam": "Not evaluated"
                }
            },
            {
                "name": "Checkly",
                "type": "Monitoring",
                "relationships": {}
            }
        ]
