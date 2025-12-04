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
    def datetime(self) -> Optional[datetime]:
        _datetime = parse(self.date)
        if not _datetime:
            raise ValueError("Could not parse date. Please use a standard format like YYYY-MM-DD")
        return _datetime

    @classmethod
    def item_type(cls) -> ZoteroItemType:
        raise NotImplementedError("No item type specified")

    @classmethod
    def bibliography_source_type(cls):
        raise NotImplementedError("No bibliography source type specified")

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
        _source_type_element = create_bibliography_namespaced_element("SourceType")
        _source_type_element.text = self.bibliography_source_type()
        _source_element.append(_source_type_element)

        if self.title:
            # <b:Title>
            _title_element = create_bibliography_namespaced_element("Title")
            _title_element.text = str(self.title)
            _source_element.append(_title_element)

        if self.creators:
            # <b:Authors>
            _author_list_element = create_bibliography_namespaced_element("Author")
            for _creator in self.creators:
                # <b:Author>
                _author_element = create_bibliography_namespaced_element("Author")
                _creator.creator_data.map_to_bibxml(_author_element)
                _author_list_element.append(_author_element)
            _source_element.append(_author_list_element)

        if self.abstract_note:
            # <b:Abstract>
            _abstract_element = create_bibliography_namespaced_element("Abstract")
            _abstract_element.text = str(self.abstract_note)
            _source_element.append(_abstract_element)

        if self.date:
            _year = self.datetime.year
            if _year:
                # <b:Year>
                _year_element = create_bibliography_namespaced_element("Year")
                _year_element.text = str(_year)
                _source_element.append(_year_element)
            _month = self.datetime.month
            if _month:
                # <b:Month>
                _month_element = create_bibliography_namespaced_element("Month")
                _month_element.text = str(_month)
                _source_element.append(_month_element)
            _day = self.datetime.day
            if _day:
                # <b:Day>
                _day_element = create_bibliography_namespaced_element("Day")
                _day_element.text = str(_day)
                _source_element.append(_day_element)
            _hour = self.datetime.hour
            if _hour:
                # <b:Hour>
                _hour_element = create_bibliography_namespaced_element("Hour")
                _hour_element.text = str(_hour)
                _source_element.append(_hour_element)
            _minute = self.datetime.minute
            if _minute:
                # <b:Minute>
                _minute_element = create_bibliography_namespaced_element("Minute")
                _minute_element.text = str(_minute)
                _source_element.append(_minute_element)
            _second = self.datetime.second
            if _second:
                # <b:Second>
                _second_element = create_bibliography_namespaced_element("Second")
                _second_element.text = str(_second)
                _source_element.append(_second_element)

        if self.language:
            # <b:Language>
            _language_element = create_bibliography_namespaced_element("Language")
            _language_element.text = str(self.language)
            _source_element.append(_language_element)

        if self.short_title:
            # <b:ShortTitle>
            _short_title_element = create_bibliography_namespaced_element("ShortTitle")
            _short_title_element.text = str(self.short_title)
            _source_element.append(_short_title_element)

        if self.url:
            # <b:URL>
            _url_element = create_bibliography_namespaced_element("URL")
            _url_element.text = str(self.url)
            _source_element.append(_url_element)

        if self.access_date:
            # <b:Accessed>
            _accessed_element = create_bibliography_namespaced_element("Accessed")
            _accessed_element.text = str(self.access_date)
            _source_element.append(_accessed_element)

        if self.archive:
            # <b:Archive>
            _archive_element = create_bibliography_namespaced_element("Archive")
            _archive_element.text = str(self.archive)
            _source_element.append(_archive_element)

        if self.archive_location:
            # <b:ArchiveLocation>
            _archive_location_element = create_bibliography_namespaced_element("ArchiveLocation")
            _archive_location_element.text = str(self.archive_location)
            _source_element.append(_archive_location_element)

        if self.library_catalog:
            # <b:LibraryCatalog>
            _library_catalog_element = create_bibliography_namespaced_element("LibraryCatalog")
            _library_catalog_element.text = str(self.library_catalog)
            _source_element.append(_library_catalog_element)

        if self.call_number:
            # <b:CallNumber>
            _call_number_element = create_bibliography_namespaced_element("CallNumber")
            _call_number_element.text = str(self.call_number)
            _source_element.append(_call_number_element)

        if self.rights:
            # <b:Rights>
            _rights_element = create_bibliography_namespaced_element("Rights")
            _rights_element.text = str(self.rights)
            _source_element.append(_rights_element)

        if self.extra:
            # <b:Comment>
            _comment_element = create_bibliography_namespaced_element("Comment")
            _comment_element.text = str(self.extra)
            _source_element.append(_comment_element)
