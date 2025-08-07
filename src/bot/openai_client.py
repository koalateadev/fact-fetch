import os

from dotenv import load_dotenv
from openai import OpenAI


def get_openai_client() -> OpenAI:
    load_dotenv()

    return OpenAI(api_key=os.environ.get('OPEN_API_KEY'))