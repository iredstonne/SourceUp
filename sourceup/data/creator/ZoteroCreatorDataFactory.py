from typing import TYPE_CHECKING, Dict, Any, Type, Tuple
if TYPE_CHECKING: from sourceup.data.creator.ZoteroBaseCreatorData import ZoteroBaseCreatorData
from sourceup.data.creator.ZoteroPersonCreatorData import ZoteroPersonCreatorData
from sourceup.data.creator.ZoteroOrganizationCreatorData import ZoteroOrganizationCreatorData

class ZoteroCreatorDataFactory:
    _REGISTRY: Tuple[Type["ZoteroBaseCreatorData"], ...] = (
        ZoteroPersonCreatorData,
        ZoteroOrganizationCreatorData,
    )

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "ZoteroBaseCreatorData":
        for creator_data_cls in cls._REGISTRY:
            if creator_data_cls.supports_data(data):
                return creator_data_cls.map_from_data(data)
        raise ValueError(f"Unhandled creator data: {data!r}")
