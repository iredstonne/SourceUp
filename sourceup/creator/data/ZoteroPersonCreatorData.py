from dataclasses import dataclass
from typing import Dict, Any, override

from sourceup.creator.ZoteroBaseCreatorData import ZoteroBaseCreatorData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroPersonCreatorData(ZoteroBaseCreatorData):
    first_name: str
    last_name: str

    @override
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def supports_data(cls, _data: Dict[str, Any]) -> bool:
        _has_first_name = "firstName" in _data
        _has_last_name = "lastName" in _data
        return _has_first_name and _has_last_name

    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroPersonCreatorData":
        first_name = map_to_str(_data.get("firstName"))
        last_name = map_to_str(_data.get("lastName"))
        return cls(first_name, last_name)
