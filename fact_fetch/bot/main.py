from fact_fetch.bot.reddit_client import get_reddit_client
from fact_fetch.bot.reddit_observer import observe_subreddit
from fact_fetch.bot.openai_client import get_openai_client
from fact_fetch.bot.openai_query import query
from fact_fetch.bot.reddit_bot import RedditBot
from fact_fetch.utils.text_normalizer import RedditTextNormalizer


def main():
    """
    Main entry point for the Fact Fetch Reddit bot.
    
    This function orchestrates the entire bot workflow:
    1. Initializes Reddit and OpenAI clients
    2. Creates bot and text normalizer instances
    3. Monitors the 'vegan' subreddit for new posts
    4. Analyzes posts for misinformation using AI
    5. Automatically responds with evidence-based counterarguments
    
    The bot processes posts with more than 100 words to ensure
    sufficient content for meaningful analysis.
    """
    reddit = get_reddit_client()
    openai = get_openai_client()
    bot = RedditBot()
    normalizer = RedditTextNormalizer()

    for i in observe_subreddit(reddit, "vegan"):
        submission = reddit.submission(i)

        # Combine title and body text for analysis
        submission_text = "title: " + submission.title + "\n body: " + submission.selftext
        
        submission_normalized = normalizer.normalize_text(submission_text)

        # Only analyze posts with sufficient content (more than 100 words)
        if submission_normalized.count(" ") > 100:
            # Use AI to analyze the post for misinformation
            result = query(openai, submission_normalized)
            print(result["result"])

            # If misinformation is detected, respond with counterargument
            if result["result"] == "misinformation":
                print(result["counterargument"])
                bot.submit_response(submission_id=submission.id, response=result["counterargument"])


if __name__ == "__main__":
    main()