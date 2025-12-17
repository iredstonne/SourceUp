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
class ZoteroDatasetItemData(ZoteroBaseItemData):
    identifier: Optional[str] = None
    type: Optional[str] = None
    version_number: Optional[str] = None
    repository: Optional[str] = None
    repository_location: Optional[str] = None
    format: Optional[str] = None
    doi: Optional[str] = None
    citation_key: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.DATASET

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "ElectronicSource"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroDatasetItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            identifier=map_to_str(_data.get("identifier")),
            type=map_to_str(_data.get("type")),
            version_number=map_to_str(_data.get("versionNumber")),
            repository=map_to_str(_data.get("repository")),
            repository_location=map_to_str(_data.get("repositoryLocation")),
            format=map_to_str(_data.get("format")),
            doi=map_to_str(_data.get("DOI")),
            citation_key=map_to_str(_data.get("citationKey")),
        )

    @override
    def map_creators_to_bibxml(self, _author_composite_element: Element):
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.AUTHOR,
            ZoteroCreatorType.CONTRIBUTOR,
        ), "Author", True)

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> ElectronicSource
        # PublicationTitle: Mapped (title)
        # City: Mapped (repository_location)
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # ProductionCompany: Mapped (repository)
        # Publisher: Mapped (repository)
        # Edition: Mapped (version_number)
        # Medium: Mapped (format)
        # Volume: Not mapped
        # StandardNumber: Mapped (identifier)
        # DOI: Mapped (doi)

        add_bibliography_namespaced_element_if_missing(_source_element, "PublicationTitle", self.title)
        add_bibliography_namespaced_element_if_missing(_source_element, "City", self.repository_location)
        add_bibliography_namespaced_element_if_missing(_source_element, "ProductionCompany", self.repository)
        add_bibliography_namespaced_element_if_missing(_source_element, "Publisher", self.repository)
        add_bibliography_namespaced_element_if_missing(_source_element, "Edition", self.version_number)
        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.format)
        add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", self.identifier)
        add_bibliography_namespaced_element_if_missing(_source_element, "DOI", self.doi)
