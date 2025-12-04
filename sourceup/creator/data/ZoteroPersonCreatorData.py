from dataclasses import dataclass
from typing import Dict, Any, override
from xml.etree.ElementTree import Element
from sourceup.creator.ZoteroBaseCreatorData import ZoteroBaseCreatorData
from sourceup.casts import map_to_str
from sourceup.exporter.wordbibxml_functions import create_bibliography_namespaced_element

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
        _first_name = map_to_str(_data.get("firstName"))
        _last_name = map_to_str(_data.get("lastName"))
        return cls(_first_name, _last_name)

    def map_to_bibxml(self, _author_element: Element):
        _name_list_element = create_bibliography_namespaced_element("NameList")
        _person_element = create_bibliography_namespaced_element("Person")
        if self.first_name:
            _first_element = create_bibliography_namespaced_element("First")
            _first_element.text = str(self.first_name)
            _person_element.append(_first_element)
        if self.last_name:
            _last_element = create_bibliography_namespaced_element("Last")
            _last_element.text = str(self.last_name)
            _person_element.append(_last_element)
        _name_list_element.append(_person_element)
        _author_element.append(_name_list_element)
