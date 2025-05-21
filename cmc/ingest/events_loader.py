class EventsLoader:
    def __init__(self, source_data=None):
        self.source = source_data

    def load(self) -> list:
        return [
            {
                "id": "RELEASE-v1.2.0",
                "type": "release",
                "tool": "Jenkins",
                "initiator": "CI Pipeline",
                "related_to": "PayrollApp",
                "timestamp": "2025-05-15T14:05:00Z",
                "tags": ["automated", "prod", "success"],
                "sub_events": ["JIRA-1234", "COMMIT-a1b2c3", "JENKINS-049"]
            },
            {
                "id": "JIRA-1234",
                "type": "ticket",
                "tool": "Jira",
                "initiator": "Jane Doe",
                "related_to": "PayrollApp",
                "timestamp": "2025-05-15T13:22:00Z",
                "tags": ["bug", "critical", "deployment"]
            },
            {
                "id": "COMMIT-a1b2c3",
                "type": "commit",
                "tool": "GitHub",
                "initiator": "Jane Doe",
                "related_to": "PayrollApp",
                "timestamp": "2025-05-15T14:00:00Z",
                "tags": ["feature", "auth"]
            },
            {
                "id": "JENKINS-049",
                "type": "deployment",
                "tool": "Jenkins",
                "initiator": "CI Pipeline",
                "related_to": "PayrollApp",
                "timestamp": "2025-05-15T14:02:00Z",
                "tags": ["success", "prod"]
            }
        ]
