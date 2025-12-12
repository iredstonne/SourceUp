from dataclasses import dataclass, field
from datetime import datetime
from typing import Tuple, Optional, Dict, Any
from xml.etree.ElementTree import Element
from dateparser import parse
from sourceup.casts import map_to_str
from sourceup.creator.ZoteroCreator import ZoteroCreator
from sourceup.exporter.wordbibxml_functions import create_bibliography_namespaced_element, \
    add_bibliography_namespaced_role_element
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
        # Language: Mapped (language)
        # ShortTitle: Mapped (short_title)
        # YearAccessed: Mapped (access_date -> year)
        # MonthAccessed: Mapped (access_date -> month)
        # DayAccessed: Mapped (access_date -> day)
        # Comments: Mapped (extra)
        # URL: Mapped (url)

        _source_type_element = create_bibliography_namespaced_element("SourceType")
        _source_type_element.text = self.bibliography_source_type()
        _source_element.append(_source_type_element)

        if self.title:
            _title_element = create_bibliography_namespaced_element("Title")
            _title_element.text = str(self.title)
            _source_element.append(_title_element)

        if self.creators:
            from sourceup.creator.ZoteroCreatorType import ZoteroCreatorType
            _author_composite_element = create_bibliography_namespaced_element("Author")

            add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
                ZoteroCreatorType.AUTHOR,
                ZoteroCreatorType.CONTRIBUTOR,
                ZoteroCreatorType.REVIEWED_AUTHOR,
                ZoteroCreatorType.COMMENTER,
                ZoteroCreatorType.PROGRAMMER,
                ZoteroCreatorType.RECIPIENT
            ), "Author", True)
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
                ZoteroCreatorType.BOOK_AUTHOR,
            ),"BookAuthor", False)
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
                ZoteroCreatorType.EDITOR,
                ZoteroCreatorType.SERIES_EDITOR
            ),"Editor", False)
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
                ZoteroCreatorType.TRANSLATOR,
            ),"Translator", False)
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
                ZoteroCreatorType.PRODUCER,
                ZoteroCreatorType.SPONSOR,
                ZoteroCreatorType.COSPONSOR
            ),"ProducerName", False)
            #add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (ZoteroCreatorType.UNKNOWN,), "Compiler", False) - No direct mapping from Zotero
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
                ZoteroCreatorType.ARTIST,
                ZoteroCreatorType.CARTOGRAPHER
            ),"Artist", False)
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators,(
                ZoteroCreatorType.COMPOSER,
            ), "Composer", False)
            #add_bibliography_namespaced_role_element(_author_composite_element, self.creators,(ZoteroCreatorType.UNKNOWN,), "Conductor", False) - No direct mapping from Zotero
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
                ZoteroCreatorType.PERFORMER,
                ZoteroCreatorType.CAST_MEMBER,
                ZoteroCreatorType.PRESENTER,
            ),"Performer", True)
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
                ZoteroCreatorType.DIRECTOR,
            ),"Director", False)
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
                ZoteroCreatorType.SCRIPT_WRITER,
                ZoteroCreatorType.WORDS_BY
            ),"Writer", False)
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators,(
                ZoteroCreatorType.INTERVIEWEE,
                ZoteroCreatorType.GUEST
            ), "Interviewee", False)
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators,(
                ZoteroCreatorType.INTERVIEWER,
                ZoteroCreatorType.PODCASTER
            ), "Interviewer", False)
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
                ZoteroCreatorType.INVENTOR,
            ),"Inventor", False)
            add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
                ZoteroCreatorType.COUNSEL,
                ZoteroCreatorType.ATTORNEY_AGENT
            ),"Counsel", False)

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
