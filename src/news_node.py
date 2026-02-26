import requests
from datetime import datetime, timedelta, timezone
from config import config

class CryptoPanicMiner:
    def __init__(self, api_key=None):
        # Fallback to config file if API key is not provided
        self.api_key = api_key or config.CRYPTOPANIC_API_KEY
        self.base_url = "https://cryptopanic.com/api/developer/v2/posts/"

    def get_recent_news(self, days_limit=None, filter_type=None, max_results=None):
        """
        Fetch news based on input parameters or fallback to default values.
        """
        days = days_limit or config.DEFAULT_NEWS_DAYS
        news_filter = filter_type or config.DEFAULT_NEWS_FILTER
        limit = max_results or config.DEFAULT_NEWS_LIMIT

        params = {
            "auth_token": self.api_key,
            "filter": news_filter,
        }

        # Calculate the cutoff time for filtering old news
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)
        collected_news = []

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            for post in data.get("results", []):
                # Parse the post creation date to a comparable timezone-aware format
                post_date = datetime.fromisoformat(post["created_at"].replace("Z", "+00:00"))                
                # Skip posts that are older than our cutoff time
                if post_date < cutoff_time:
                    continue
                
                # Extract the relevant information for the AI agent
                collected_news.append({
                    "title": post.get("title"),
                    "domain": post.get("domain"),
                    "date": post_date.strftime("%Y-%m-%d %H:%M"),
                    "votes": post.get("votes", {}) # Includes user sentiment votes (bullish/bearish)
                })

                if len(collected_news) >= limit:
                    break

            return collected_news

        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return []