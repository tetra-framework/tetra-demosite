from demo.models import BreakingNews
from tetra import public, ReactiveComponent


class NewsTicker(ReactiveComponent):
    headline: str = public("")
    # could be a fixed subscription too:
    # subscription = "notifications.news.headline"

    def load(self, *args, **kwargs) -> None:
        # Fetch random news headline from database
        self.headline = BreakingNews.objects.all().order_by("?").first().title
