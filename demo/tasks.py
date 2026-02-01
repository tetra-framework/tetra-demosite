import asyncio
from tetra.dispatcher import ComponentDispatcher


async def send_breaking_news_to_channel():
    from demo.models import BreakingNews

    while True:
        news = await BreakingNews.objects.all().order_by("?").afirst()
        print("Sending breaking news:", news.title)
        await ComponentDispatcher.data_updated(
            "notifications.news.headline",
            data={
                "headline": news.title,
            },
        )
        await asyncio.sleep(10)
