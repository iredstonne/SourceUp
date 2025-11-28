from typing import TYPE_CHECKING, Tuple, Type
if TYPE_CHECKING: from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.item.data.ZoteroBookItemData import ZoteroBookItemData
from sourceup.item.data.ZoteroBookSectionItemData import ZoteroBookSectionItemData
from sourceup.item.data.ZoteroManuscriptItemData import ZoteroManuscriptItemData
from sourceup.item.data.ZoteroThesisItemData import ZoteroThesisItemData
from sourceup.item.data.ZoteroReportItemData import ZoteroReportItemData
from sourceup.item.data.ZoteroEncyclopediaArticleItemData import ZoteroEncyclopediaArticleItemData
from sourceup.item.data.ZoteroJournalArticleItemData import ZoteroJournalArticleItemData
from sourceup.item.data.ZoteroNewspaperArticleItemData import ZoteroNewspaperArticleItemData
from sourceup.item.data.ZoteroMagazineArticleItemData import ZoteroMagazineArticleItemData
from sourceup.item.data.ZoteroArtworkItemData import ZoteroArtworkItemData
from sourceup.item.data.ZoteroPodcastItemData import ZoteroPodcastItemData
from sourceup.item.data.ZoteroInterviewItemData import ZoteroInterviewItemData
from sourceup.item.data.ZoteroFilmItemData import ZoteroFilmItemData
from sourceup.item.data.ZoteroAudioRecordingItemData import ZoteroAudioRecordingItemData
from sourceup.item.data.ZoteroVideoRecordingItemData import ZoteroVideoRecordingItemData
from sourceup.item.data.ZoteroRadioBroadcastItemData import ZoteroRadioBroadcastItemData
from sourceup.item.data.ZoteroTvBroadcastItemData import ZoteroTvBroadcastItemData
from sourceup.item.data.ZoteroPresentationItemData import ZoteroPresentationItemData
from sourceup.item.data.ZoteroConferencePaperItemData import ZoteroConferencePaperItemData
from sourceup.item.data.ZoteroWebpageItemData import ZoteroWebpageItemData
from sourceup.item.data.ZoteroBlogPostItemData import ZoteroBlogPostItemData
from sourceup.item.data.ZoteroForumPostItemData import ZoteroForumPostItemData
from sourceup.item.data.ZoteroEmailItemData import ZoteroEmailItemData
from sourceup.item.data.ZoteroInstantMessageItemData import ZoteroInstantMessageItemData
from sourceup.item.data.ZoteroDatasetItemData import ZoteroDatasetItemData
from sourceup.item.data.ZoteroComputerProgramItemData import ZoteroComputerProgramItemData
from sourceup.item.data.ZoteroDocumentItemData import ZoteroDocumentItemData
from sourceup.item.data.ZoteroPreprintItemData import ZoteroPreprintItemData
from sourceup.item.data.ZoteroAttachmentItemData import ZoteroAttachmentItemData
from sourceup.item.data.ZoteroDictionaryEntryItemData import ZoteroDictionaryEntryItemData

class ZoteroItemDataRegistry:
    ENTRIES: Tuple[Type["ZoteroBaseItemData"], ...] = (
        ZoteroBookItemData,
        ZoteroBookSectionItemData,
        ZoteroManuscriptItemData,
        ZoteroThesisItemData,
        ZoteroReportItemData,
        ZoteroEncyclopediaArticleItemData,
        ZoteroJournalArticleItemData,
        ZoteroNewspaperArticleItemData,
        ZoteroMagazineArticleItemData,
        ZoteroArtworkItemData,
        ZoteroPodcastItemData,
        ZoteroInterviewItemData,
        ZoteroFilmItemData,
        ZoteroAudioRecordingItemData,
        ZoteroVideoRecordingItemData,
        ZoteroRadioBroadcastItemData,
        ZoteroTvBroadcastItemData,
        ZoteroPresentationItemData,
        ZoteroConferencePaperItemData,
        ZoteroWebpageItemData,
        ZoteroBlogPostItemData,
        ZoteroForumPostItemData,
        ZoteroEmailItemData,
        ZoteroInstantMessageItemData,
        ZoteroDatasetItemData,
        ZoteroComputerProgramItemData,
        ZoteroDocumentItemData,
        ZoteroAttachmentItemData,
        ZoteroPreprintItemData,
        ZoteroDictionaryEntryItemData
    )
