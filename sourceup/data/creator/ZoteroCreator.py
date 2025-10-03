from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Any
if TYPE_CHECKING: from sourceup.data.creator.ZoteroBaseCreatorData import ZoteroBaseCreatorData
from sourceup.data.creator.ZoteroCreatorType import ZoteroCreatorType

@dataclass(frozen=True, slots=True)
class ZoteroCreator:
    creator_type: ZoteroCreatorType
    creator_data: ZoteroBaseCreatorData

    @property
    def is_person(self) -> bool:
        from sourceup.data.creator.ZoteroPersonCreatorData import ZoteroPersonCreatorData
        return isinstance(self.creator_data, ZoteroPersonCreatorData)

    @property
    def is_organization(self) -> bool:
        from sourceup.data.creator.ZoteroOrganizationCreatorData import ZoteroOrganizationCreatorData
        return isinstance(self.creator_data, ZoteroOrganizationCreatorData)

    @classmethod
    def map_from_data(cls, data: Dict[str, Any]) -> "ZoteroCreator":
        creator_type = ZoteroCreatorType(data.get("creatorType"))
        from sourceup.data.creator.ZoteroCreatorDataFactory import ZoteroCreatorDataFactory
        creator_data = ZoteroCreatorDataFactory.from_data(data)
        return cls(creator_type, creator_data)
