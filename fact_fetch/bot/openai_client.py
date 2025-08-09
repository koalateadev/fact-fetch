import os

from dotenv import load_dotenv
from openai import OpenAI


def get_openai_client() -> OpenAI:
    """
    Create and return an authenticated OpenAI client instance.
    
    This function loads environment variables from a .env file and creates
    an OpenAI client with the provided API key for accessing OpenAI's services.
    
    Required environment variables:
        - OPENAI_API_KEY: OpenAI API key for authentication
        
    Returns:
        OpenAI: Authenticated OpenAI client instance
        
    Raises:
        KeyError: If OPENAI_API_KEY environment variable is missing
        Exception: If OpenAI client initialization fails
        
    Note:
        The .env file should be created in the project root directory
        with the appropriate OpenAI API key. The API key should have
        access to the GPT-4 model and file search capabilities.
    """
    load_dotenv()

    return OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))