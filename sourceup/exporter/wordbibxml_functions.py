from typing import Iterable, Optional, Any
from sourceup.creator.ZoteroCreator import ZoteroCreator, ZoteroCreatorType
from sourceup.item.ZoteroItem import ZoteroItem
from xml.etree.ElementTree import register_namespace, Element, ElementTree

BIBLIOGRAPHY_NS = "http://schemas.openxmlformats.org/officeDocument/2006/bibliography"
register_namespace("b", BIBLIOGRAPHY_NS)

def find_bibliography_namespaced_element(_source_element: Element, _tag_name: str) -> Optional[Element]:
    return _source_element.find(f"{{{BIBLIOGRAPHY_NS}}}{_tag_name}")

def create_bibliography_namespaced_element(_tag_name: str) -> Element:
    return Element(f"{{{BIBLIOGRAPHY_NS}}}{_tag_name}")

def add_bibliography_namespaced_element_if_missing(_source_element: Element, _tag_name: str, _tag_value: Any):
    if _tag_value:
        _element = find_bibliography_namespaced_element(
            _source_element, _tag_name)
        if _element:
            _element.text = str(_tag_value)
        else:
            _element = create_bibliography_namespaced_element(_tag_name)
            _element.text = str(_tag_value)
            _source_element.append(_element)

def add_bibliography_namespaced_role_element(_author_composite_element: Element, _creators: Iterable[ZoteroCreator], _role_applicable_creator_types: Iterable[ZoteroCreatorType], _role_element_name: str, _include_corporate_roles: bool):
    if not _creators:
        return
    _role_applicable_creator_types = set(_role_applicable_creator_types)
    _role_creators = [
        _creator for _creator in _creators
        if _creator.creator_type in _role_applicable_creator_types
    ]
    if not _role_creators:
        return
    from sourceup.creator.data.ZoteroPersonCreatorData import ZoteroPersonCreatorData
    _person_role_creators = [
        _role_creator for _role_creator in _role_creators
        if isinstance(_role_creator.creator_data, ZoteroPersonCreatorData)
    ]
    _corporate_role_creators = []
    if _include_corporate_roles:
        from sourceup.creator.data.ZoteroCorporateCreatorData import ZoteroCorporateCreatorData
        _corporate_role_creators = [
            _role_creator for _role_creator in _role_creators
            if isinstance(_role_creator.creator_data, ZoteroCorporateCreatorData)
        ]
    if not _person_role_creators and not _corporate_role_creators:
        return
    _role_element = create_bibliography_namespaced_element(_role_element_name)
    if _corporate_role_creators:
        _corporate_role_creators[0].creator_data.map_to_bibxml(_role_element)
    elif _person_role_creators:
        _name_list_element = create_bibliography_namespaced_element("NameList")
        for _creator in _person_role_creators:
            _creator.creator_data.map_to_bibxml(_name_list_element)
        _role_element.append(_name_list_element)
    if list(_role_element):
        _author_composite_element.append(_role_element)

def export_as_bibxml_to_output_file(_items: Iterable[ZoteroItem], _output_file_save_path: str) -> str:
    _sources_element = create_bibliography_namespaced_element("Sources")
    for _item in _items:
        _source_element = create_bibliography_namespaced_element("Source")
        _tag_element = create_bibliography_namespaced_element("Tag")
        _tag_element.text = _item.item_key
        _source_element.append(_tag_element)
        _item.item_data.map_to_bibxml(_source_element)
        _sources_element.append(_source_element)
    _tree = ElementTree(_sources_element)
    _tree.write(_output_file_save_path, xml_declaration=True, encoding="UTF-8")
    return _output_file_save_path

def decipher_bibxml_export_error(e: Exception) -> str:
    if isinstance(e, (OSError, IOError)):
        return "Unable to write BibXML export file to file system"
    return str(e)
