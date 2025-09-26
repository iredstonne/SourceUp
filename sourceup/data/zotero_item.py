from dataclasses import dataclass


@dataclass
class ZoteroItem:
    key: str
    title: str
    creator_names: list[str]
    date: str
    link: str

