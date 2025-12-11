from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroPresentationItemData(ZoteroBaseItemData):
    presentation_type: Optional[str] = None
    place: Optional[str] = None
    meeting_name: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.PRESENTATION

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Misc"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroPresentationItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            presentation_type=map_to_str(_data.get("presentationType")),
            place=map_to_str(_data.get("place")),
            meeting_name=map_to_str(_data.get("meetingName"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Misc
        # PublicationTitle: Mapped (meeting_name)
        # MediaType: Mapped "Presentation"
        # City: Mapped (city)
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # Publisher: Not mapped
        # Pages: Not mapped
        # Volume: Not mapped
        # Edition: Not mapped
        # Number: Not mapped
        # StandardNumber: Not mapped
        # Medium: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "PublicationTitle", self.meeting_name)
        add_bibliography_namespaced_element_if_missing(_source_element, "City", self.place)
        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.presentation_type)

