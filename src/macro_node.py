import feedparser

class MacroMiner:
    def __init__(self, rss_urls=None):
        self.rss_urls = rss_urls or [
            "https://bankless.substack.com/feed",
            "https://thedefiedge.substack.com/feed"
        ]

    def get_latest_macro(self, limit_per_feed=2):
        collected_macro = []

        for url in self.rss_urls:
            try:
                feed = feedparser.parse(url)
                source_name = feed.feed.get("title", "Unknown Source")

                # کلمه limit_per_feed در اینجا اصلاح شد
                for entry in feed.entries[:limit_per_feed]:
                    raw_summary = entry.get("summary", "")
                    
                    collected_macro.append({
                        "source": source_name,
                        "title": entry.get("title", "No Title"),
                        "date": entry.get("published", "Unknown Date"),
                        "summary": raw_summary[:400] + "..." 
                    })

            except Exception as e:
                print(f"Error fetching from {url}: {e}")

        return collected_macro