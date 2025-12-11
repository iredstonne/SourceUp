from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroBillItemData(ZoteroBaseItemData):
    bill_number: Optional[str] = None
    code: Optional[str] = None
    code_volume: Optional[str] = None
    section: Optional[str] = None
    code_pages: Optional[str] = None
    legislative_body: Optional[str] = None
    session: Optional[str] = None
    history: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.BILL

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Misc"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroBillItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            bill_number=map_to_str(_data.get("billNumber")),
            code=map_to_str(_data.get("code")),
            code_volume=map_to_str(_data.get("codeVolume")),
            section=map_to_str(_data.get("section")),
            code_pages=map_to_str(_data.get("codePages")),
            legislative_body=map_to_str(_data.get("legislativeBody")),
            session=map_to_str(_data.get("session")),
            history=map_to_str(_data.get("history"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Misc
        # PublicationTitle: Mapped (code)
        # MediaType: Mapped "Bill"
        # City: Not mapped
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # Publisher: Mapped (legislative_body)
        # Pages: Mapped (code_pages)
        # Volume: Mapped (code_volume)
        # Edition: Mapped (session)
        # Number: Mapped (bill_number)
        # StandardNumber: Mapped (bill_number)
        # Medium: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "PublicationTitle", self.code)
        add_bibliography_namespaced_element_if_missing(_source_element, "MediaType", "Bill")
        add_bibliography_namespaced_element_if_missing(_source_element, "Publisher", self.legislative_body)
        add_bibliography_namespaced_element_if_missing(_source_element, "Pages", self.code_pages)
        add_bibliography_namespaced_element_if_missing(_source_element, "Volume", self.code_volume)
        add_bibliography_namespaced_element_if_missing(_source_element, "Edition", self.session)
        add_bibliography_namespaced_element_if_missing(_source_element, "Number", self.bill_number)
        add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", self.bill_number)
