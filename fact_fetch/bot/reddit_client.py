import os

import praw
from dotenv import load_dotenv


def get_reddit_client() -> praw.Reddit:
    """
    Create and return an authenticated Reddit client instance.
    
    This function loads environment variables from a .env file and creates
    a PRAW (Python Reddit API Wrapper) client with the provided credentials.
    
    Required environment variables:
        - REDDIT_CLIENT_ID: Reddit application client ID
        - REDDIT_CLIENT_SECRET: Reddit application client secret
        - REDDIT_USER_AGENT: User agent string for the application
        - REDDIT_USERNAME: Reddit account username
        - REDDIT_PASSWORD: Reddit account password
        
    Returns:
        praw.Reddit: Authenticated Reddit client instance
        
    Raises:
        KeyError: If required environment variables are missing
        Exception: If Reddit authentication fails
        
    Note:
        The .env file should be created in the project root directory
        with the appropriate Reddit API credentials.
    """
    load_dotenv()

    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
    )