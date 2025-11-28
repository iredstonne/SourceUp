from dataclasses import dataclass
from typing import Dict, Any, override

from sourceup.creator.ZoteroBaseCreatorData import ZoteroBaseCreatorData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroOrganizationCreatorData(ZoteroBaseCreatorData):
    name: str

    @override
    def display_name(self) -> str:
        return f"{self.name}"

    @classmethod
    def supports_data(cls, _data: Dict[str, Any]) -> bool:
        _has_name = "name" in _data
        return _has_name

    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroOrganizationCreatorData":
        _name = map_to_str(_data.get("name"))
        return cls(_name)
