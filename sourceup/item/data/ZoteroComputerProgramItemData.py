from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.creator.ZoteroCreatorType import ZoteroCreatorType
from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing, \
    add_bibliography_namespaced_role_element
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroComputerProgramItemData(ZoteroBaseItemData):
    series_title: Optional[str] = None
    version_number: Optional[str] = None
    system: Optional[str] = None
    place: Optional[str] = None
    company: Optional[str] = None
    programming_language: Optional[str] = None
    isbn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.COMPUTER_PROGRAM

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "ElectronicSource"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroComputerProgramItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            series_title=map_to_str(_data.get("seriesTitle")),
            version_number=map_to_str(_data.get("versionNumber")),
            system=map_to_str(_data.get("system")),
            place=map_to_str(_data.get("place")),
            company=map_to_str(_data.get("company")),
            programming_language=map_to_str(_data.get("programmingLanguage")),
            isbn=map_to_str(_data.get("ISBN"))
        )

    @override
    def map_creators_to_bibxml(self, _author_composite_element: Element):
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.PROGRAMMER,
            ZoteroCreatorType.CONTRIBUTOR,
        ), "Author", True)

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> ElectronicSource
        # PublicationTitle: Mapped (series_title)
        # City: Mapped (place)
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # ProductionCompany: Mapped (company)
        # Publisher: Mapped (company)
        # Edition: Mapped (version_number)
        # Medium: Mapped (system)
        # Volume: Not mapped
        # StandardNumber: Mapped (isbn)
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "PublicationTitle", self.series_title)
        add_bibliography_namespaced_element_if_missing(_source_element, "City", self.place)
        add_bibliography_namespaced_element_if_missing(_source_element, "ProductionCompany", self.company)
        add_bibliography_namespaced_element_if_missing(_source_element, "Publisher", self.company)
        add_bibliography_namespaced_element_if_missing(_source_element, "Edition", self.version_number)
        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.system)
        add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", self.isbn)
