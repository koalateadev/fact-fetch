import logging
from datetime import datetime

from fact_fetch.bot.reddit_client import get_reddit_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedditBot:
    """
    A Reddit bot class that handles posting and responding to Reddit submissions.
    
    This class provides functionality to:
    - Authenticate with Reddit API
    - Reply to existing submissions with counterarguments
    - Create new text posts (useful for testing)
    
    All operations are logged for monitoring and debugging purposes.
    """

    def __init__(self):
        """
        Initialize the RedditBot instance.
        
        Creates a Reddit client connection and verifies authentication.
        Logs the authenticated username for confirmation.
        
        Raises:
            Exception: If Reddit client initialization fails
        """
        try:
            self.reddit = get_reddit_client()
            logger.info(f"Successfully authenticated as {self.reddit.user.me()}")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit instance: {str(e)}")
            raise

    def submit_response(self, submission_id: str, response: str):
        """
        Reply to an existing Reddit submission with a counterargument.
        
        Args:
            submission_id (str): The Reddit submission ID to reply to
            response (str): The counterargument text to post as a reply
            
        Raises:
            Exception: If the reply submission fails
            
        Note:
            This method is used by the main bot to respond to posts
            containing misinformation with evidence-based counterarguments.
        """
        try:
            # Get the submission object and post the reply
            submission = self.reddit.submission(submission_id)
            submission.reply(response)
            logger.info(f"Successfully replied to post: {submission.url}")
        except Exception as e:
            logger.error(f"Failed to submit response: {str(e)}")
            raise

    def submit_post(self, subreddit_name: str, title: str, content: str):
        """
        Create a new text post in a specified subreddit.
        
        Args:
            subreddit_name (str): Name of the subreddit to post to
            title (str): Title of the post
            content (str): Body text content of the post
            
        Returns:
            praw.models.Submission: The created submission object
            
        Raises:
            Exception: If the post creation fails
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            submission = subreddit.submit(
                title=title,
                selftext=content
            )
            logger.info(f"Successfully created text post: {submission.url}")

            return submission

        except Exception as e:
            logger.error(f"Failed to submit post: {str(e)}")
            raise

def main():
    """
    Test function to verify Reddit bot functionality.
    
    Creates a test post in the 'test' subreddit to ensure that:
    - Reddit authentication is working
    - The bot can successfully post content
    - All logging is functioning properly
    
    This function is useful for debugging and verifying bot setup.
    """
    try:
        poster = RedditBot()

        subreddit = "test"  # Use 'test' subreddit for testing
        title = f"Test post - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        content = "This is a test post created using PRAW!"
        draft = poster.submit_draft(subreddit, title, content)
        print(f"Post successfully created: {draft.url}")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()