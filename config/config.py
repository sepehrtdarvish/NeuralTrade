import os
from dotenv import load_dotenv
# Metis AI Gateway Configuration
# Tip: Set the METIS_API_KEY environment variable in your terminal before running.

load_dotenv()
METIS_API_KEY = os.getenv("METIS_API_KEY")
# The custom endpoint provided by Metis documentation
API_ENDPOINT = "https://api.tapsage.com"

# The designated Gemini model
MODEL_NAME = "gemini-2.0-flash"

# The prompt to send to the model
USER_PROMPT = "Explain the concept of decorators in Python in simple terms."


YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

# Crypto Panic
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY")

DEFAULT_NEWS_DAYS = 1
DEFAULT_NEWS_FILTER = "hot"
DEFAULT_NEWS_LIMIT = 20