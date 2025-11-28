from pyzotero.zotero import Zotero
from sourceup.client.zotero.BaseZoteroClientConfig import BaseZoteroClientConfig

class PyZoteroClientConfig(BaseZoteroClientConfig[Zotero]):
    def create_client(self) -> Zotero:
        return Zotero(
            library_type=self._library.library_type,
            library_id=self._library.library_id,
            api_key=self._library.private_key or None
        )
