from dataclasses import dataclass

@dataclass
class GoogleFile:

    def __init__(self, name, id, parents):
        self.name = name
        self.id = id
        self.parents = parents