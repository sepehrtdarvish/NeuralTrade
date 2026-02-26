import feedparser
from datetime import datetime
import time

class ResearchMiner:
    def __init__(self, rss_url=None):
        # Default to Glassnode Insights (Top-tier on-chain analysis)
        self.rss_url = rss_url or "https://insights.glassnode.com/rss/"

    def get_latest_research(self, limit=5):
        """
        Fetch the latest on-chain research articles from the RSS feed.
        """
        collected_research = []

        try:
            # Parse the RSS feed
            feed = feedparser.parse(self.rss_url)
            
            # Check if feed was parsed successfully
            if feed.bozo:
                print(f"Warning: Issue parsing the feed: {feed.bozo_exception}")

            for entry in feed.entries[:limit]:
                # Extract the summary/description (usually contains the core analysis)
                # We clean up basic HTML tags if they exist in the summary
                raw_summary = entry.get("summary", "")
                
                # Some feeds use 'published', others use 'updated'
                published_date = entry.get("published", entry.get("updated", "Unknown Date"))

                collected_research.append({
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", ""),
                    "date": published_date,
                    "summary": raw_summary[:500] + "..." if len(raw_summary) > 500 else raw_summary
                })

            return collected_research

        except Exception as e:
            print(f"Error fetching research data: {e}")
            return []