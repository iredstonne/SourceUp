import warnings
from enum import StrEnum


class ZoteroCreatorType(StrEnum):
    ARTIST = "artist"
    ATTORNEY_AGENT = "attorneyAgent"
    AUTHOR = "author"
    BOOK_AUTHOR = "bookAuthor"
    CARTOGRAPHER = "cartographer"
    CAST_MEMBER = "castMember"
    COMMENTER = "commenter"
    COMPOSER = "composer"
    CONTRIBUTOR = "contributor"
    COSPONSOR = "cosponsor"
    COUNSEL = "counsel"
    DIRECTOR = "director"
    EDITOR = "editor"
    GUEST = "guest"
    INTERVIEWEE = "interviewee"
    INTERVIEWER = "interviewer"
    INVENTOR = "inventor"
    PERFORMER = "performer"
    PODCASTER = "podcaster"
    PRESENTER = "presenter"
    PRODUCER = "producer"
    PROGRAMMER = "programmer"
    RECIPIENT = "recipient"
    REVIEWED_AUTHOR = "reviewedAuthor"
    SCRIPT_WRITER = "scriptwriter"
    SERIES_EDITOR = "seriesEditor"
    SPONSOR = "sponsor"
    TRANSLATOR = "translator"
    WORDS_BY = "wordsBy"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, value: object) -> "ZoteroCreatorType":
        warnings.warn(f"Unhandled creator type: {value!r}")
        return ZoteroCreatorType.UNKNOWN
