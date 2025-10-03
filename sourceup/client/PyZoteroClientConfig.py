from dataclasses import dataclass
from pyzotero.zotero import Zotero
from sourceup.client.ZoteroBaseClientConfig import ZoteroBaseClientConfig

@dataclass
class PyZoteroClientConfig(ZoteroBaseClientConfig[Zotero]):
    def create_client(self) -> Zotero:
        return Zotero(
            library_type=self.library.library_type,
            library_id=self.library.library_id,
            api_key=self.library.private_key
        )
