import typing_extensions

from aiovkapi.types.methods.base_category import BaseCategory
from aiovkapi.types.methods import *

if typing_extensions.TYPE_CHECKING:
    import aiovkapi


class APICategories(BaseCategory):

    def __init__(self, api: "aiovkapi.API"):
        super(APICategories, self).__init__(api)
        self.ads = AdsCategory(api)
        self.app_widgets = AppWidgetsCategory(api)
        self.groups = GroupsCategory(api)
        self.gifts = GiftsCategory(api)
        self.video = VideoCategory(api)
        self.notes = NotesCategory(api)
        self.newsfeed = NewsfeedCategory(api)
        self.donut = DonutCategory(api)
        self.pages = PagesCategory(api)
        self.search = SearchCategory(api)
        self.polls = PollsCategory(api)
        self.status = StatusCategory(api)
        self.streaming = StreamingCategory(api)
        self.fave = FaveCategory(api)
        self.messages = MessagesCategory(api)
        self.docs = DocsCategory(api)
        self.widgets = WidgetsCategory(api)
        self.adsweb = AdswebCategory(api)
        self.pretty_cards = PrettyCardsCategory(api)
        self.board = BoardCategory(api)
        self.database = DatabaseCategory(api)
        self.likes = LikesCategory(api)
        self.lead_forms = LeadFormsCategory(api)
        self.downloaded_games = DownloadedGamesCategory(api)
        self.market = MarketCategory(api)
        self.stories = StoriesCategory(api)
        self.friends = FriendsCategory(api)
        self.podcasts = PodcastsCategory(api)
        self.apps = AppsCategory(api)
        self.storage = StorageCategory(api)
        self.store = StoreCategory(api)
        self.orders = OrdersCategory(api)
        self.stats = StatsCategory(api)
        self.wall = WallCategory(api)
        self.account = AccountCategory(api)
        self.users = UsersCategory(api)
        self.secure = SecureCategory(api)
        self.auth = AuthCategory(api)
        self.photos = PhotosCategory(api)
        self.utils = UtilsCategory(api)
        self.notifications = NotificationsCategory(api)
