class ServersLoader:
    def __init__(self, source_data=None):
        self.source = source_data

    def load(self) -> list:
        return [
            {
                "vlan_name": "V-45",
                "subnet": "145.223.45.1",
                "gateway": "145.223.45.1",
                "broadcast": "145.223.45.100"                
            },
             {
                "vlan_name": "V-46",
                "subnet": "145.223.46.0",
                "gateway": "145.223.46.11",
                "broadcast": "145.223.45.98"                
            }
        ]
