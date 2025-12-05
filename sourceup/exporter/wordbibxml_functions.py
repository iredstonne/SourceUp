from typing import Iterable, Optional, Any
from sourceup.item.ZoteroItem import ZoteroItem
from xml.etree.ElementTree import register_namespace, Element, ElementTree

BIBLIOGRAPHY_NS = "http://schemas.openxmlformats.org/officeDocument/2006/bibliography"
register_namespace("b", BIBLIOGRAPHY_NS)

def create_bibliography_namespaced_element(_tag_name: str) -> Element:
    return Element(f"{{{BIBLIOGRAPHY_NS}}}{_tag_name}")

def find_bibliography_namespaced_element(_source_element: Element, _tag_name: str) -> Optional[Element]:
    return _source_element.find(f"{{{BIBLIOGRAPHY_NS}}}{_tag_name}")

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

def add_common_book_bibliography_namespaced_elements(
    _source_element: Element,
    _volume,
    _number_volumes,
    _edition,
    _city,
    _publisher,
    _pages,
    _standard_number
):
    add_bibliography_namespaced_element_if_missing(_source_element, "Volume", _volume)
    add_bibliography_namespaced_element_if_missing(_source_element, "NumberVolumes", _number_volumes)
    add_bibliography_namespaced_element_if_missing(_source_element, "Edition", _edition)
    add_bibliography_namespaced_element_if_missing(_source_element, "City", _city)
    add_bibliography_namespaced_element_if_missing(_source_element, "Publisher", _publisher)
    add_bibliography_namespaced_element_if_missing(_source_element, "Pages", _pages)
    add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", _standard_number)

def export_as_bibxml_to_output_file(_items: Iterable[ZoteroItem], _output_file_save_path: str) -> str:
    # <b:Sources>
    _sources_element = create_bibliography_namespaced_element("Sources")
    for _item in _items:
        # <b:Source>
        _source_element = create_bibliography_namespaced_element("Source")
        # <b:Tag>
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
