from dataclasses import dataclass
from typing import Dict, Any
from sourceup.casts import map_to_str
from sourceup.data.creator.ZoteroBaseCreatorData import ZoteroBaseCreatorData

@dataclass(frozen=True, slots=True)
class ZoteroOrganizationCreatorData(ZoteroBaseCreatorData):
    name: str

    @classmethod
    def supports_data(cls, data: Dict[str, Any]) -> bool:
        return "name" in data

    @classmethod
    def map_from_data(cls, data: Dict[str, Any]) -> "ZoteroOrganizationCreatorData":
        _name = map_to_str(data.get("name"))
        return cls(_name)
