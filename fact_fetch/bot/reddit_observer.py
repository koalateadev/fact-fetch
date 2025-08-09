import praw

from fact_fetch.bot.reddit_client import get_reddit_client


def observe_subreddit(reddit: praw.Reddit, subreddit_name: str):
    """
    Create a stream of new submissions from a specified subreddit.
    
    This function sets up a real-time stream that yields new submissions
    as they are posted to the specified subreddit. The stream will
    continuously monitor for new posts and return them as they appear.
    
    Args:
        reddit (praw.Reddit): Authenticated Reddit client instance
        subreddit_name (str): Name of the subreddit to monitor
        
    Returns:
        praw.models.util.stream_generator: A generator that yields new submissions
        
    Note:
        This function uses Reddit's streaming API which provides real-time
        updates. The stream will continue indefinitely until interrupted.
        Each yielded item is a submission ID that can be used to get
        the full submission object.
    """
    subreddit = reddit.subreddit(subreddit_name)

    return subreddit.stream.submissions()


if __name__ == '__main__':
    """
    Test function to verify subreddit observation functionality.
    
    Tests the observe_subreddit function by monitoring the "PlantBasedDiet"
    subreddit and printing details of new submissions to verify the
    streaming functionality works correctly.
    """
    reddit = get_reddit_client()

    for i in observe_subreddit(reddit, "PlantBasedDiet"):
        print("result: " + str(i))
        print(reddit.submission(i).title)
        print(reddit.submission(i).selftext)