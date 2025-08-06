import praw
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

from reddit_client import get_reddit_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedditBot:

    def __init__(self):
        try:
            self.reddit = get_reddit_client()
            logger.info(f"Successfully authenticated as {self.reddit.user.me()}")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit instance: {str(e)}")
            raise

    def submit_draft(self, subreddit_name: str, title: str, content: str):
        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            submission = subreddit.submit(
                title=title,
                selftext=content
            )
            logger.info(f"Successfully created draft text post: {submission.url}")

            return submission

        except Exception as e:
            logger.error(f"Failed to submit draft: {str(e)}")
            raise

def main():
    try:
        poster = RedditBot()

        subreddit = "test"  # Use 'test' subreddit for testing
        title = f"Test post - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        content = "This is a test post created using PRAW!"
        draft = poster.submit_draft(subreddit, title, content)
        print(f"Draft successfully created: {draft.url}")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()