from enum import Enum, auto
from dataclasses import dataclass

class LibraryType(int, Enum):
    USER = auto()
    GROUP = auto()

@dataclass(frozen=True, slots=True)
class ZoteroLibrary:
    library_type: LibraryType
    id: str
    private_key: str | None

    def __repr__(self):
        return f"ZoteroLibrary({self.library_type.name}, {self.id}, {"Private" if self.private_key else "Public"})"

    def __str__(self):
        return self.__repr__()
