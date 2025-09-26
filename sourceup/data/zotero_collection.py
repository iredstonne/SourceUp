from dataclasses import dataclass

@dataclass
class ZoteroCollection:
    key: str
    name: str

    def __repr__(self):
        return self.name or "Untitled"
