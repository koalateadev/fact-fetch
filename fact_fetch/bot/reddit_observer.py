import praw

from fact_fetch.bot.reddit_client import get_reddit_client


def observe_subreddit(reddit: praw.Reddit, subreddit_name: str):
    subreddit = reddit.subreddit(subreddit_name)

    return subreddit.stream.submissions()

if __name__ == '__main__':
    reddit = get_reddit_client()

    for i in observe_subreddit(reddit, "PlantBasedDiet"):
        print("result: " + str(i))
        print(reddit.submission(i).title)
        print(reddit.submission(i).selftext)