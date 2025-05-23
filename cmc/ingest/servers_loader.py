class ServersLoader:
    def __init__(self, source_data=None):
        self.source = source_data

    def load(self) -> list:
        return [
            {
                "hostname": "VM-PAY-01",
                "environment": "prod",
                "IP Address": "145.223.45.6",
                "runs": ["PayrollApp"],
                "subnet": ["V-45"]
            },
             {
                "hostname": "VM-PAY-02",
                "environment": "staging",
                "IP Address": "145.223.46.0",
                "runs": ["PayrollApp"],
                "subnet": ["V-46"]
             }
        ]
