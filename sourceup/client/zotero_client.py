import json

from pyzotero import zotero
from sourceup.data.zotero_collection import ZoteroCollection
from sourceup.data.zotero_item import ZoteroItem
from sourceup.data.zotero_library import ZoteroLibrary, LibraryType


def _zotero(library: ZoteroLibrary):
    return zotero.Zotero(
        library.library_id,
        "user" if library.library_type == LibraryType.USER else "group",
        library.private_key or None,
    )

def fetch_collections(library: ZoteroLibrary):
    z = _zotero(library)
    collections = []
    for collection in z.everything(z.collections()):
        key = (collection.get("key") or "").strip()
        data = (collection.get("data") or {})
        name = (data.get("name") or "").strip()
        #print(json.dumps(data, indent=4))
        collections.append(ZoteroCollection(
            key,
            name
        ))
    return collections

def fetch_items_from_collection(library: ZoteroLibrary, collection: ZoteroCollection):
    z = _zotero(library)
    items = []
    for item in z.everything(z.collection_items(collection.key)):
        key = (item.get("key") or "").strip()
        data = (item.get("data") or {})
        #print(json.dumps(data, indent=4))
        title = (data.get("title") or "").strip()
        creators = (data.get("creators") or [])
        creators_names = []
        for creator in creators:
            if isinstance(creator, dict):
                continue
            creator_name = (creator.get("name") or "").strip()
            if creator_name:
                creators_names.append(creator_name)
                continue
            first_name = (creator.get("first_name") or "").strip()
            last_name = (creator.get("last_name") or "").strip()
            creator_name = first_name + " " + last_name
            if creator_name:
                creators_names.append(creator_name)
        date = (data.get("date") or "").strip()
        link = (data.get("url") or "").strip()
        items.append(ZoteroItem(
            key,
            title,
            creators_names,
            date,
            link
        ))
    return items
