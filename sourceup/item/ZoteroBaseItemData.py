from dataclasses import dataclass, field
from datetime import datetime
from typing import Tuple, Optional, Dict, Any
from xml.etree.ElementTree import Element
from dateparser import parse
from sourceup.casts import map_to_str
from sourceup.creator.ZoteroCreator import ZoteroCreator
from sourceup.exporter.wordbibxml_functions import create_bibliography_namespaced_element
from sourceup.item.ZoteroItemType import ZoteroItemType


@dataclass(frozen=True, slots=True)
class ZoteroBaseItemData:
    title: str
    creators: Tuple["ZoteroCreator", ...] = field(default_factory=tuple)
    abstract_note: Optional[str] = None
    date: Optional[str] = None
    language: Optional[str] = None
    short_title: Optional[str] = None
    url: Optional[str] = None
    access_date: Optional[str] = None
    archive: Optional[str] = None
    archive_location: Optional[str] = None
    library_catalog: Optional[str] = None
    call_number: Optional[str] = None
    rights: Optional[str] = None
    extra: Optional[str] = None

    @property
    def date_to_datetime(self) -> Optional[datetime]:
        return parse(self.date)

    @property
    def access_date_to_datetime(self) -> Optional[datetime]:
        return parse(self.access_date)

    @classmethod
    def item_type(cls) -> ZoteroItemType:
        raise NotImplementedError("No item type specified")

    @classmethod
    def bibliography_source_type(cls):
        return "Misc"

    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroBaseItemData":
        return cls(
            title=map_to_str(_data.get("title")),
            creators=tuple(ZoteroCreator.map_from_data(_creator_data) for _creator_data in _data.get("creators") or ()),
            abstract_note=map_to_str(_data.get("abstractNote")),
            date=map_to_str(_data.get("date")),
            language=map_to_str(_data.get("language")),
            short_title=map_to_str(_data.get("shortTitle")),
            url=map_to_str(_data.get("url")),
            access_date=map_to_str(_data.get("accessDate")),
            archive=map_to_str(_data.get("archive")),
            archive_location=map_to_str(_data.get("archiveLocation")),
            library_catalog=map_to_str(_data.get("libraryCatalog")),
            call_number=map_to_str(_data.get("callNumber")),
            rights=map_to_str(_data.get("rights")),
            extra=map_to_str(_data.get("extra"))
        )

    def map_to_bibxml(self, _source_element: Element):
        # SourceType: Mapped (delegated)
        # Creators: Partially mapped (not delegated yet)
        # Title: Mapped (title)
        # Year: Mapped (date -> year)
        # Month: Mapped (date -> month)
        # Day: Mapped (date -> day)
        # Language: Mapped
        # ShortTitle: Mapped
        # YearAccessed: Mapped (access_date -> year)
        # MonthAccessed: Mapped (access_date -> month)
        # DayAccessed: Mapped (access_date -> day)
        # Comments: Mapped
        # URL: Mapped

        _source_type_element = create_bibliography_namespaced_element("SourceType")
        _source_type_element.text = self.bibliography_source_type()
        _source_element.append(_source_type_element)

        if self.title:
            # <b:Title>
            _title_element = create_bibliography_namespaced_element("Title")
            _title_element.text = str(self.title)
            _source_element.append(_title_element)

        if self.creators:
            from sourceup.creator.ZoteroCreatorType import ZoteroCreatorType
            from sourceup.creator.data.ZoteroPersonCreatorData import ZoteroPersonCreatorData
            from sourceup.creator.data.ZoteroCorporateCreatorData import ZoteroCorporateCreatorData

            _author_composite_element = create_bibliography_namespaced_element("Author")

            # Role: Author
            _author_creators = [
                _creator for _creator in self.creators
                if _creator.creator_type == ZoteroCreatorType.AUTHOR
            ]

            if _author_creators:
                _corporate_author_creators = [
                    _author_creator for _author_creator in _author_creators
                    if isinstance(_author_creator.creator_data, ZoteroCorporateCreatorData)
                ]
                _person_author_creators = [
                    _author_creator for _author_creator in _author_creators
                    if isinstance(_author_creator.creator_data, ZoteroPersonCreatorData)
                ]

                _author_role_element = create_bibliography_namespaced_element("Author")

                if _corporate_author_creators:
                    _corporate_author_creators[0].creator_data.map_to_bibxml(_author_role_element)
                elif _person_author_creators:
                    _name_list_element = create_bibliography_namespaced_element("NameList")

                    for _creator in _person_author_creators:
                        _creator.creator_data.map_to_bibxml(_name_list_element)

                    _author_role_element.append(_name_list_element)

                if list(_author_role_element):
                    _author_composite_element.append(_author_role_element)

            # Role: Book Author
            _book_author_creators = [
                _creator for _creator in self.creators
                if _creator.creator_type == ZoteroCreatorType.AUTHOR
            ]

            if _book_author_creators:
                _person_book_author_creators = [
                    _book_author_creator for _book_author_creator in _book_author_creators
                    if isinstance(_book_author_creator.creator_data, ZoteroPersonCreatorData)
                ]

                _book_author_role_element = create_bibliography_namespaced_element("Bookauthor")

                if _person_book_author_creators:
                    _name_list_element = create_bibliography_namespaced_element("NameList")

                    for _creator in _person_book_author_creators:
                        _creator.creator_data.map_to_bibxml(_name_list_element)

                    _book_author_role_element.append(_name_list_element)

                if list(_book_author_role_element):
                    _author_composite_element.append(_book_author_role_element)

            # Role: Editor
            _editor_creators = [
                _creator for _creator in self.creators
                if _creator.creator_type == ZoteroCreatorType.EDITOR
            ]

            if _editor_creators:
                _person_editor_creators = [
                    _editor_creator for _editor_creator in _editor_creators
                    if isinstance(_editor_creator.creator_data, ZoteroPersonCreatorData)
                ]

                _editor_role_element = create_bibliography_namespaced_element("Editor")

                if _person_editor_creators:
                    _name_list_element = create_bibliography_namespaced_element("NameList")

                    for _creator in _person_editor_creators:
                        _creator.creator_data.map_to_bibxml(_name_list_element)

                    _editor_role_element.append(_name_list_element)

                if list(_editor_role_element):
                    _author_composite_element.append(_editor_role_element)

            # Role: Producer
            _producer_creators = [
                _creator for _creator in self.creators
                if _creator.creator_type == ZoteroCreatorType.PRODUCER
            ]

            if _producer_creators:
                _person_producer_creators = [
                    _producer_creator for _producer_creator in _producer_creators
                    if isinstance(_producer_creator.creator_data, ZoteroPersonCreatorData)
                ]

                _producer_role_element = create_bibliography_namespaced_element("Producer")

                if _person_producer_creators:
                    _name_list_element = create_bibliography_namespaced_element("NameList")

                    for _creator in _person_producer_creators:
                        _creator.creator_data.map_to_bibxml(_name_list_element)

                    _producer_role_element.append(_name_list_element)

                if list(_producer_role_element):
                    _author_composite_element.append(_producer_role_element)

            # Role: Artist
            _artist_creators = [
                _creator for _creator in self.creators
                if _creator.creator_type == ZoteroCreatorType.ARTIST
            ]

            if _artist_creators:
                _person_artist_creators = [
                    _artist_creator for _artist_creator in _artist_creators
                    if isinstance(_artist_creator.creator_data, ZoteroPersonCreatorData)
                ]

                _artist_role_element = create_bibliography_namespaced_element("Artist")

                if _person_artist_creators:
                    _name_list_element = create_bibliography_namespaced_element("NameList")

                    for _creator in _person_artist_creators:
                        _creator.creator_data.map_to_bibxml(_name_list_element)

                    _artist_role_element.append(_name_list_element)

                if list(_artist_role_element):
                    _author_composite_element.append(_artist_role_element)

            # Role: Director
            _director_creators = [
                _creator for _creator in self.creators
                if _creator.creator_type == ZoteroCreatorType.DIRECTOR
            ]

            if _director_creators:
                _person_director_creators = [
                    _performer_creator for _performer_creator in _director_creators
                    if isinstance(_performer_creator.creator_data, ZoteroPersonCreatorData)
                ]

                _director_role_element = create_bibliography_namespaced_element("Director")

                if _person_director_creators:
                    _name_list_element = create_bibliography_namespaced_element("NameList")

                    for _creator in _person_director_creators:
                        _creator.creator_data.map_to_bibxml(_name_list_element)

                    _director_role_element.append(_name_list_element)

                if list(_director_role_element):
                    _author_composite_element.append(_director_role_element)

            # Role: Performer
            _performer_creators = [
                _creator for _creator in self.creators
                if _creator.creator_type == ZoteroCreatorType.PERFORMER
            ]

            if _performer_creators:
                _person_performer_creators = [
                    _performer_creator for _performer_creator in _performer_creators
                    if isinstance(_performer_creator.creator_data, ZoteroPersonCreatorData)
                ]

                _performer_role_element = create_bibliography_namespaced_element("Performer")

                if _person_performer_creators:
                    _name_list_element = create_bibliography_namespaced_element("NameList")

                    for _creator in _person_performer_creators:
                        _creator.creator_data.map_to_bibxml(_name_list_element)

                    _performer_role_element.append(_name_list_element)

                if list(_performer_role_element):
                    _author_composite_element.append(_performer_role_element)

            # Role: Inventor
            _inventor_creators = [
                _creator for _creator in self.creators
                if _creator.creator_type == ZoteroCreatorType.INVENTOR
            ]

            if _inventor_creators:
                _person_inventor_creators = [
                    _inventor_creator for _inventor_creator in _inventor_creators
                    if isinstance(_inventor_creator.creator_data, ZoteroPersonCreatorData)
                ]

                _inventor_role_element = create_bibliography_namespaced_element("Inventor")

                if _person_inventor_creators:
                    _name_list_element = create_bibliography_namespaced_element("NameList")

                    for _creator in _person_inventor_creators:
                        _creator.creator_data.map_to_bibxml(_name_list_element)

                    _inventor_role_element.append(_name_list_element)

                if list(_inventor_role_element):
                    _author_composite_element.append(_inventor_role_element)

            if list(_author_composite_element):
                _source_element.append(_author_composite_element)

        if self.date_to_datetime:
            _year = self.date_to_datetime.year
            if _year:
                _year_element = create_bibliography_namespaced_element("Year")
                _year_element.text = str(_year)
                _source_element.append(_year_element)
            _month = self.date_to_datetime.month
            if _month:
                _month_element = create_bibliography_namespaced_element("Month")
                _month_element.text = str(_month)
                _source_element.append(_month_element)
            _day = self.date_to_datetime.day
            if _day:
                _day_element = create_bibliography_namespaced_element("Day")
                _day_element.text = str(_day)
                _source_element.append(_day_element)

        if self.language:
            _lcid_element = create_bibliography_namespaced_element("LCID")
            _lcid_element.text = str(self.language)
            _source_element.append(_lcid_element)

        if self.short_title:
            _short_title_element = create_bibliography_namespaced_element("ShortTitle")
            _short_title_element.text = str(self.short_title)
            _source_element.append(_short_title_element)

        if self.access_date_to_datetime:
            _year_accessed = self.access_date_to_datetime.year
            if _year_accessed:
                _year_accessed_element = create_bibliography_namespaced_element("YearAccessed")
                _year_accessed_element.text = str(_year_accessed)
                _source_element.append(_year_accessed_element)
            _month_accessed = self.access_date_to_datetime.month
            if _month_accessed:
                _month_accessed_element = create_bibliography_namespaced_element("MonthAccessed")
                _month_accessed_element.text = str(_month_accessed)
                _source_element.append(_month_accessed_element)
            _day_accessed = self.access_date_to_datetime.day
            if _day_accessed:
                _day_accessed_element = create_bibliography_namespaced_element("DayAccessed")
                _day_accessed_element.text = str(_day_accessed)
                _source_element.append(_day_accessed_element)

        if self.extra:
            _comments_element = create_bibliography_namespaced_element("Comments")
            _comments_element.text = str(self.extra)
            _source_element.append(_comments_element)

        if self.url:
            _url_element = create_bibliography_namespaced_element("URL")
            _url_element.text = str(self.url)
            _source_element.append(_url_element)
