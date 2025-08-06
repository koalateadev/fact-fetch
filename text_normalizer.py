import re
from typing import Optional
from unicodedata import normalize as unicode_normalize
from bs4 import BeautifulSoup
import emoji


def valid_submission(text) -> bool:
    if text is not None and len(text) > 0:
        return True
    else:
        return False


class RedditTextNormalizer:
    def __init__(self):
        # Common Reddit-specific patterns
        self.reddit_patterns = {
            'subreddit': r'/r/\w+',
            'user': r'/u/\w+',
            'url': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            'markdown_links': r'\[([^\]]+)\]\(([^)]+)\)',
            'markdown_formatting': r'[\*\_\~\`]{1,3}',
            'html_entities': r'&[a-z]+;',
        }

    def remove_urls(self, text: str) -> str:
        """Remove URLs from text."""
        return re.sub(self.reddit_patterns['url'], ' ', text)

    def remove_reddit_formatting(self, text: str) -> str:
        """Remove Reddit-specific formatting."""
        # Remove subreddit references
        text = re.sub(self.reddit_patterns['subreddit'], ' ', text)
        # Remove user mentions
        text = re.sub(self.reddit_patterns['user'], ' ', text)
        # Remove markdown links
        text = re.sub(self.reddit_patterns['markdown_links'], r'\1', text)
        # Remove markdown formatting characters
        text = re.sub(self.reddit_patterns['markdown_formatting'], '', text)
        return text

    def remove_html(self, text: str) -> str:
        """Remove HTML tags and entities."""
        # Remove HTML tags
        text = BeautifulSoup(text, 'html.parser').get_text()
        # Remove HTML entities
        text = re.sub(self.reddit_patterns['html_entities'], ' ', text)
        return text

    def remove_deleted(self, text: str) -> str:
        """Remove removed and deleted posts."""
        return text.replace("[removed]", "").replace("[deleted]", "")

    def remove_emojis(self, text: str) -> str:
        """Remove emojis from text."""
        return emoji.replace_emoji(text, '')

    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace characters."""
        # Replace newlines and tabs with spaces
        text = re.sub(r'[\n\t\r]+', ' ', text)
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def normalize_unicode(self, text: str) -> str:
        """Normalize Unicode characters."""
        # Convert to ASCII where possible
        return unicode_normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

    def normalize_text(self, text: Optional[str], lowercase: bool = True) -> str:
        """
        Main function to normalize Reddit submission text.

        Args:
            text: Input text to normalize
            lowercase: Whether to convert text to lowercase

        Returns:
            Normalized text string
        """
        if not text:
            return ""

        # Convert to string if needed
        text = str(text)

        # Apply normalization steps
        text = self.remove_html(text)
        text = self.remove_urls(text)
        text = self.remove_reddit_formatting(text)
        text = self.remove_emojis(text)
        text = self.remove_deleted(text)
        text = self.normalize_unicode(text)
        text = self.normalize_whitespace(text)

        if lowercase:
            text = text.lower()

        return text
