import warnings
from enum import StrEnum

class ZoteroItemType(StrEnum):
    BOOK = "book"
    BOOK_SECTION = "bookSection"
    MANUSCRIPT = "manuscript"
    THESIS = "thesis"
    REPORT = "report"
    PREPRINT = "preprint"
    DOCUMENT = "document"
    MAP = "map"
    JOURNAL_ARTICLE = "journalArticle"
    MAGAZINE_ARTICLE = "magazineArticle"
    NEWSPAPER_ARTICLE = "newspaperArticle"
    ENCYCLOPEDIA_ARTICLE = "encyclopediaArticle"
    DICTIONARY_ENTRY = "dictionaryEntry"
    STANDARD = "standard"
    CONFERENCE_PAPER = "conferencePaper"
    PRESENTATION = "presentation"
    ARTWORK = "artwork"
    FILM = "film"
    AUDIO_RECORDING = "audioRecording"
    VIDEO_RECORDING = "videoRecording"
    RADIO_BROADCAST = "radioBroadcast"
    TV_BROADCAST = "tvBroadcast"
    PODCAST = "podcast"
    INTERVIEW = "interview"
    WEBPAGE = "webpage"
    BLOG_POST = "blogPost"
    FORUM_POST = "forumPost"
    DATASET = "dataset"
    COMPUTER_PROGRAM = "computerProgram"
    EMAIL = "email"
    INSTANT_MESSAGE = "instantMessage"
    LETTER = "letter"
    NOTE = "note"
    ATTACHMENT = "attachment"
    STATUTE = "statute"
    BILL = "bill"
    CASE = "case"
    HEARING = "hearing"
    PATENT = "patent"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, _value: object) -> "ZoteroItemType":
        warnings.warn(f"Unhandled item type: {_value!r}")
        return ZoteroItemType.UNKNOWN
