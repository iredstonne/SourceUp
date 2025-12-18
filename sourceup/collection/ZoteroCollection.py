from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ZoteroCollection:
    collection_key: str
    collection_name: str

    @property
    def model_name(self):
        return self.collection_name
