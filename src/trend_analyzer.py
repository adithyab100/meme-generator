import praw
from typing import List, Dict

class TrendAnalyzer:
    def __init__(self, config):
        self.reddit = praw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            user_agent=config.REDDIT_USER_AGENT
        )
    
    def get_trending_topics(self, subreddit: str = "memes", limit: int = 10) -> List[Dict]:
        """Get trending topics from Reddit."""
        trending = []
        for post in self.reddit.subreddit(subreddit).hot(limit=limit):
            trending.append({
                "title": post.title,
                "score": post.score,
                "url": post.url
            })
        return trending