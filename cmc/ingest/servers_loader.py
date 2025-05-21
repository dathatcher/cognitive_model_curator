class ServersLoader:
    def __init__(self, source_data=None):
        self.source = source_data

    def load(self) -> list:
        return [
            {
                "hostname": "VM-PAY-01",
                "environment": "prod",
                "runs": ["PayrollApp"],
                "monitored_by": []
            }
        ]
