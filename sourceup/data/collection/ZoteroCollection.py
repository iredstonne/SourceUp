from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ZoteroCollection:
    key: str
    name: str

    def __repr__(self):
        return f"ZoteroCollection({self.key}, {self.name})"

    def __str__(self):
        return self.__repr__()
