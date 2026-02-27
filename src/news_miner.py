import requests
import feedparser
import logging
import newspaper
from newspaper import Article
from datetime import datetime, timedelta, timezone
from time import mktime
from config import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewsMiner:
    def __init__(self, feeds=None, days_limit=None):
        self.feeds = feeds or config.BITCOIN_RSS_FEEDS
        self.days_limit = days_limit or config.DEFAULT_NEWS_DAYS
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }

    def _parse_date(self, entry) -> datetime:
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            return datetime.fromtimestamp(mktime(entry.published_parsed), timezone.utc)
        return datetime.now(timezone.utc)

    def _extract_full_text(self, url: str) -> str:
        """ورود به لینک و استخراج متن کامل مقاله"""
        if not url:
            return ""
        try:
            # اعمال هدر برای جلوگیری از بلاک شدن توسط سایت‌ها
            config_np = newspaper.Config()
            config_np.browser_user_agent = self.headers["User-Agent"]
            config_np.request_timeout = 10
            
            article = Article(url, config=config_np)
            article.download()
            article.parse()
            return article.text.strip()
        except Exception as e:
            logging.warning(f"Failed to extract text from {url}: {e}")
            return ""

    def get_strategic_news(self) -> list:
        collected_news = []
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=self.days_limit)

        for feed_url in self.feeds:
            logging.info(f"Fetching RSS feed: {feed_url}")
            try:
                response = requests.get(feed_url, headers=self.headers, timeout=10)
                response.raise_for_status()

                parsed_feed = feedparser.parse(response.text)
                
                if getattr(parsed_feed, 'bozo', 0) == 1:
                    logging.warning(f"Malformed feed detected/parsed for: {feed_url}")

                source_name = parsed_feed.feed.get("title", feed_url)

                for entry in parsed_feed.entries:
                    post_date = self._parse_date(entry)
                    
                    if post_date < cutoff_time:
                        continue 

                    url = entry.get("link", "")
                    
                    # استخراج متن کامل
                    full_text = self._extract_full_text(url)
                    
                    # اگر نتوانست متن را بگیرد یا متن خالی بود، آن خبر را نادیده بگیر
                    if not full_text:
                        continue

                    collected_news.append({
                        "title": entry.get("title", ""),
                        "full_text": full_text,  # جایگزین description شد
                        "url": url,           
                        "published_at": post_date.isoformat(),
                        "source": source_name,
                        "kind": "news"
                    })

            except requests.exceptions.RequestException as e:
                logging.error(f"Network/Timeout error for {feed_url}: {e}")
            except Exception as e:
                logging.error(f"Failed to parse feed {feed_url}: {e}")

        collected_news.sort(key=lambda x: x["published_at"], reverse=True)
        return collected_news
