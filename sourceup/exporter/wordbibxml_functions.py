from typing import Iterable
from sourceup.item.ZoteroItem import ZoteroItem
from xml.etree.ElementTree import register_namespace, Element, SubElement, ElementTree

BIBLIOGRAPHY_NS = "http://schemas.openxmlformats.org/officeDocument/2006/bibliography"
register_namespace("b", BIBLIOGRAPHY_NS)

def create_bibliography_namespaced_element(_tag_name: str):
    return Element(f"{{{BIBLIOGRAPHY_NS}}}{_tag_name}")

def create_bibliography_namespaced_sub_element(_parent_element: Element, _tag_name: str):
    return SubElement(_parent_element, f"{{{BIBLIOGRAPHY_NS}}}{_tag_name}")

def create_bibxml_sources_element() -> Element:
    return create_bibliography_namespaced_element("Sources")

def create_bibxml_source_element(_item: ZoteroItem) -> Element:
    _source_element = create_bibliography_namespaced_element("Source")
    _tag_element = create_bibliography_namespaced_sub_element(_source_element, "Tag")
    _tag_element.text = _item.item_key
    _item.item_data.map_to_bibxml(_source_element)
    return _source_element

def export_as_bibxml_to_output_file(_items: Iterable[ZoteroItem], _output_file_save_path: str):
    # <b:Sources>
    _sources_element = create_bibxml_sources_element()
    for _item in _items:
        # <b:Source>
        _source_element = create_bibxml_source_element(_item)
        _sources_element.append(_source_element)
    _tree = ElementTree(_sources_element)
    _tree.write(_output_file_save_path, xml_declaration=True, encoding="UTF-8")
    return _output_file_save_path

def decipher_bibxml_export_error(e: Exception) -> str:
    if isinstance(e, (OSError, IOError)):
        return "Unable to write BibXML to disk"
    return str(e)
