import os
from dotenv import load_dotenv
# Metis AI Gateway Configuration
# Tip: Set the METIS_API_KEY environment variable in your terminal before running.

load_dotenv()
METIS_API_KEY = os.getenv("METIS_API_KEY")
# The custom endpoint provided by Metis documentation
API_ENDPOINT = "https://api.tapsage.com"

# The designated Gemini model
SUMMARIES_MODEL_NAME = "gemini-2.0-flash"
ANALYSIS_MODEL_NAME ="gemini-2.0-flash"

# The prompt to send to the model
DEFAULT_NEWS_DAYS = 2  # دریافت اخبار تا چند روز گذشته
    
    # لیست بهترین فیدهای RSS اختصاصی و کلان برای بیت‌کوین
BITCOIN_RSS_FEEDS = [
    "https://cointelegraph.com/rss/tag/bitcoin",
    "https://bitcoinmagazine.com/feed",
    "https://decrypt.co/feed",
    "https://www.newsbtc.com/feed/",
    #"https://www.coindesk.com/arc/outboundfeeds/rss/"
]
