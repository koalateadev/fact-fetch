from reddit_client import get_reddit_client
from reddit_observer import observe_subreddit
from openai_client import get_openai_client
from openai_query import query
from reddit_bot import RedditBot
from text_normalizer import RedditTextNormalizer


def main():
    reddit = get_reddit_client()
    openai = get_openai_client()
    bot = RedditBot()
    normalizer = RedditTextNormalizer()

    for i in observe_subreddit(reddit, "vegan"):
        submission = reddit.submission(i)

        # TODO if time is older submission.created_utc, time.time()

        submission_text = "title: " + submission.title + "\n\n body: " + submission.selftext
        submission_normalized = normalizer.normalize_text(submission_text)

        if submission_normalized.count(" ") > 100:
            result = query(openai, submission_normalized)
            print(result["result"])

            if result["result"] == "misinformation":
                print(result["counterargument"])
                bot.submit_response(submission_id=submission.id, response=result["counterargument"])


if __name__ == "__main__":
    main()