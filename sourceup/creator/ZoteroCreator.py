from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Any
if TYPE_CHECKING: from sourceup.creator.ZoteroBaseCreatorData import ZoteroBaseCreatorData
from sourceup.creator.ZoteroCreatorType import ZoteroCreatorType

@dataclass(frozen=True, slots=True)
class ZoteroCreator:
    creator_type: ZoteroCreatorType
    creator_data: "ZoteroBaseCreatorData"

    @property
    def is_person(self) -> bool:
        from sourceup.creator.data.ZoteroPersonCreatorData import ZoteroPersonCreatorData
        return isinstance(self.creator_data, ZoteroPersonCreatorData)

    @property
    def is_organization(self) -> bool:
        from sourceup.creator.data.ZoteroCorporateCreatorData import ZoteroCorporateCreatorData
        return isinstance(self.creator_data, ZoteroCorporateCreatorData)

    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroCreator":
        _creator_type = ZoteroCreatorType(_data.get("creatorType"))
        from sourceup.creator.ZoteroCreatorDataFactory import ZoteroCreatorDataFactory
        _creator_data = ZoteroCreatorDataFactory.from_data(_data)
        return cls(_creator_type, _creator_data)

    def __repr__(self):
        _display_name = self.creator_data.display_name().strip()
        _role = self.creator_type.name.strip().replace("_", " ").title()
        return f"{_display_name} ({_role})"

    def __str__(self):
        return self.__repr__()

