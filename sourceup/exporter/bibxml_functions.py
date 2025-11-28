from typing import Iterable
from sourceup.item.ZoteroItem import ZoteroItem

def export_items_as_bibxml(selected_collection_items: Iterable[ZoteroItem], output_file_save_path: str):
    print(selected_collection_items)
    return output_file_save_path

def decipher_bibxml_export_error(e: Exception) -> str:
    return str(e)
