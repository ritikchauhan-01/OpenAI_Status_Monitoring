import asyncio
import aiohttp
import feedparser
from dateutil import parser as date_parser, tz
from bs4 import BeautifulSoup


PRODUCT_MAP = {
    "API": [
        "Chat Completions",
        "Responses",
        "Embeddings",
        "Fine-tuning",
        "Images",
        "Batch",
        "Audio",
        "Moderations",
        "Realtime",
        "Files",
        "Login",
        "Sora"
    ],
    "ChatGPT": [
        "Conversations",
        "Login",
        "Compliance API",
        "Search",
        "File uploads",
        "Voice mode",
        "GPTs",
        "Image Generation",
        "Deep Research",
        "Agent",
        "Codex",
        "ChatGPT Atlas",
        "Connectors/Apps"
    ],
    "Sora": [
        "Login",
        "Video generation",
        "Video viewing",
        "Feed",
        "Image Generation"
    ]
}


class StatusMonitor:
    def __init__(self, feed_url):
        self.feed_url = feed_url
        self.etag = None
        self.last_modified = None
        self.seen_entries = set()

    async def fetch_and_process(self, session):
        headers = {}

        if self.etag:
            headers["If-None-Match"] = self.etag
        if self.last_modified:
            headers["If-Modified-Since"] = self.last_modified

        try:
            async with session.get(self.feed_url, headers=headers) as response:
                if response.status == 304:
                    return

                self.etag = response.headers.get("ETag")
                self.last_modified = response.headers.get("Last-Modified")

                raw_feed = await response.text()
                self.process_feed(raw_feed)

        except Exception as e:
            print(f"Error: {e}")

    def extract_component(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        li_tag = soup.find("li")

        return (
            li_tag.get_text().split("(")[0].strip()
            if li_tag
            else ""
        )

    def get_main_product(self, sub_component):
        sub_component_lower = sub_component.lower()

        for product, components in PRODUCT_MAP.items():
            for comp in components:
                if comp.lower() in sub_component_lower:
                    return product

        return ""

    def process_feed(self, raw_feed):
        feed = feedparser.parse(raw_feed)

        for entry in reversed(feed.entries):
            if entry.id in self.seen_entries:
                continue

            self.seen_entries.add(entry.id)

            published_time = date_parser.parse(entry.published).astimezone(
                tz.gettz("Asia/Kolkata")
            )
            formatted_time = published_time.strftime("%Y-%m-%d %H:%M:%S")

            component = self.extract_component(entry.description)
            main_product = self.get_main_product(component)
            status_title = entry.title.strip()

            # 🔥 ORIGINAL FORMAT RESTORED
            print(f"[{formatted_time}] Product: OpenAI {main_product} - {component}")
            print(f"Status: {status_title}\n")


async def monitor_all(feeds, interval=60):
    monitors = [StatusMonitor(feed) for feed in feeds]

    timeout = aiohttp.ClientTimeout(total=15)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        while True:
            tasks = [monitor.fetch_and_process(session) for monitor in monitors]
            await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(interval)


if __name__ == "__main__":
    FEED_URLS = [
        "https://status.openai.com/history.rss",
        # Add more feeds here
    ]

    print("Listening for status updates...\n")
    asyncio.run(monitor_all(FEED_URLS, interval=60))