from dataclasses import dataclass

@dataclass
class GoogleFile:

    def __init__(self, name, id, parents):
        self.name = name
        self.id = id
        self.parents = parents

@dataclass
class GoogleApiClientHttpError:

    def __init__(self, code, message, status, details):
        self.code = code
        self.message = message
        self.status = status
        self.details = details
