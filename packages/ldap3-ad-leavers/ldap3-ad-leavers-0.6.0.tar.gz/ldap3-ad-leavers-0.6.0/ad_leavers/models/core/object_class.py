from datetime import datetime

# > This is the ObjectClass model
# > This is the Parent class for all AD objects
class ObjectClass:

    def __init__(self, name: str, distinguished_name: str, when_created: datetime):
        self.name = name
        self.when_created = when_created
        self.distinguished_name = distinguished_name