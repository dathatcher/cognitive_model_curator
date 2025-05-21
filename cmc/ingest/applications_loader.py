class ApplicationsLoader:
    def __init__(self, source_data=None):
        self.source = source_data

    def load(self) -> list:
        return [
            {
                "name": "PayrollApp",
                "environments": ["prod", "staging"],
                "deployed_on": ["VM-PAY-01", "VM-PAY-02"],
                "owned_by": "HR Dev Team",
                "monitored_by": ["Datadog"]
            }
        ]
