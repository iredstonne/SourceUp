from dataclasses import dataclass
from typing import Dict, Any, override
from xml.etree.ElementTree import Element
from sourceup.creator.ZoteroBaseCreatorData import ZoteroBaseCreatorData
from sourceup.casts import map_to_str
from sourceup.exporter.wordbibxml_functions import create_bibliography_namespaced_element

@dataclass(frozen=True, slots=True)
class ZoteroCorporateCreatorData(ZoteroBaseCreatorData):
    name: str

    @override
    def display_name(self) -> str:
        return f"{self.name}"

    @classmethod
    def supports_data(cls, _data: Dict[str, Any]) -> bool:
        _has_name = "name" in _data
        return _has_name

    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroCorporateCreatorData":
        _name = map_to_str(_data.get("name"))
        return cls(_name)

    def map_to_bibxml(self, _author_element: Element):
        _corporate_element = create_bibliography_namespaced_element("Corporate")
        if self.name:
            _name_element = create_bibliography_namespaced_element("Name")
            _name_element.text = self.name
            _corporate_element.append(_name_element)
        _author_element.append(_corporate_element)
