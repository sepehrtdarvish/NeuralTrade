import logging
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.errors import (
    TranscriptsDisabled, 
    NoTranscriptFound, 
    VideoUnavailable
)

# Set up logging for production visibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

class YouTubeSentimentMiner:
    """
    A tool to fetch metadata and transcripts for recent YouTube videos 
    from a specified list of channels.
    """
    
    def __init__(self, api_key, channel_ids, days_limit):
        """
        Initializes the YouTubeSentimentMiner.
        
        Args:
            api_key (str): Your YouTube Data API v3 key.
            channel_ids (List[str]): List of YouTube Channel IDs.
            days_limit (int): Number of days to look back for recent videos.
        """
        self.api_key = config.YOUTUBE_API_KEY
        self.channel_ids = config.YOUTUBE_IDS
        self.days_limit = config.YOUTUBE_DAYS 
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        
    def _get_cutoff_date(self) -> str:
        """Calculates the UTC cutoff date for fetching videos in RFC 3339 format."""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=self.days_limit)
        return cutoff_date.isoformat()

    def _get_recent_videos(self, channel_id: str, published_after: str) -> List[Dict]:
        """Fetches recent video metadata for a specific channel using the Search API."""
        videos = []
        try:
            # Note: The search endpoint costs 100 quota units per request.
            request = self.youtube.search().list(
                part="snippet",
                channelId=channel_id,
                publishedAfter=published_after,
                maxResults=50, 
                type="video",
                order="date"
            )
            response = request.execute()
            
            for item in response.get("items", []):
                videos.append({
                    "video_id": item["id"]["videoId"],
                    "video_title": item["snippet"]["title"],
                    "publish_date": item["snippet"]["publishedAt"],
                    "channel_name": item["snippet"]["channelTitle"]
                })
        except HttpError as e:
            logger.error(f"YouTube API error for channel {channel_id}: {e}")
            
        return videos

    def _get_transcript(self, video_id: str) -> Optional[str]:
        """Fetches and concatenates the transcript for a given video ID."""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            # Combine all transcript segments into a single continuous string
            return " ".join([entry['text'] for entry in transcript_list])
        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
            logger.warning(f"Transcript unavailable for video {video_id} ({type(e).__name__}).")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching transcript for video {video_id}: {e}")
            return None

    def get_recent_data(self) -> List[Dict]:
        """
        Fetches metadata and transcripts for recent videos across all initialized channels.
        
        Returns:
            List[Dict]: A list containing channel_name, video_title, publish_date, and transcript_text.
        """
        published_after = self._get_cutoff_date()
        mined_data = []

        logger.info(f"Looking up videos published after {published_after} across {len(self.channel_ids)} channel(s).")

        for channel_id in self.channel_ids:
            logger.info(f"Processing channel ID: {channel_id}")
            recent_videos = self._get_recent_videos(channel_id, published_after)
            
            for video in recent_videos:
                logger.debug(f"Fetching transcript for: {video['video_title']}")
                transcript_text = self._get_transcript(video['video_id'])
                
                mined_data.append({
                    "channel_name": video["channel_name"],
                    "video_title": video["video_title"],
                    "publish_date": video["publish_date"],
                    "transcript_text": transcript_text
                })
                
        logger.info(f"Data mining complete. Processed {len(mined_data)} videos.")
        return mined_data
7
    
"""    # Instantiate the miner
    miner = YouTubeSentimentMiner(
        api_key=API_KEY, 
        channel_ids=TARGET_CHANNELS, 
        days_limit=DAYS
    )
    
    # Execute the fetching process
    results = miner.get_recent_data()
    
    # Display the structured results
    print("\n--- MINED DATA PREVIEW ---")
    for res in results:
        print(f"\nChannel: {res['channel_name']}")
        print(f"Title:   {res['video_title']}")
        print(f"Date:    {res['publish_date']}")
        
        # Truncate transcript text for cleaner terminal output
        transcript = res['transcript_text']
        if transcript:
            display_text = f"{transcript[:150]}..."
        else:
            display_text = "[No transcript available]"
            
        print(f"Text:    {display_text}")"""