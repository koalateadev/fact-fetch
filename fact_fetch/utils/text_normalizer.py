import re
from typing import Optional
from unicodedata import normalize as unicode_normalize
from bs4 import BeautifulSoup
import emoji


class RedditTextNormalizer:
    """
    A utility class for cleaning and normalizing Reddit text content.
    
    This class provides methods to remove Reddit-specific formatting,
    HTML tags, URLs, emojis, and other elements that might interfere
    with AI text analysis. It ensures that text is clean and consistent
    for processing by the fact-checking AI.
    
    The normalizer handles:
    - Reddit-specific formatting (subreddit links, user mentions, markdown)
    - HTML tags and entities
    - URLs and links
    - Emojis and special characters
    - Unicode normalization
    - Whitespace normalization
    """
    
    def __init__(self):
        """
        Initialize the RedditTextNormalizer with regex patterns.
        
        Sets up common Reddit-specific regex patterns for identifying
        and removing various types of formatting and content.
        """
        # Common Reddit-specific patterns for text cleaning
        self.reddit_patterns = {
            'subreddit': r'/r/\w+',  # Subreddit references like /r/vegan
            'user': r'/u/\w+',       # User mentions like /u/username
            'url': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # URLs
            'markdown_links': r'\[([^\]]+)\]\(([^)]+)\)',  # Markdown links [text](url)
            'markdown_formatting': r'[\*\_\~\`]{1,3}',     # Bold, italic, strikethrough, code
            'html_entities': r'&[a-z]+;',                  # HTML entities like &amp;
        }

    def remove_urls(self, text: str) -> str:
        """
        Remove URLs from text content.
        
        Args:
            text (str): Input text that may contain URLs
            
        Returns:
            str: Text with URLs replaced by spaces
        """
        return re.sub(self.reddit_patterns['url'], ' ', text)

    def remove_reddit_formatting(self, text: str) -> str:
        """
        Remove Reddit-specific formatting elements.
        
        This method removes subreddit references, user mentions,
        markdown links, and formatting characters that are specific
        to Reddit's markdown system.
        
        Args:
            text (str): Input text with Reddit formatting
            
        Returns:
            str: Text with Reddit formatting removed
        """
        # Remove subreddit references (e.g., /r/vegan)
        text = re.sub(self.reddit_patterns['subreddit'], ' ', text)
        # Remove user mentions (e.g., /u/username)
        text = re.sub(self.reddit_patterns['user'], ' ', text)
        # Remove markdown links but keep the link text
        text = re.sub(self.reddit_patterns['markdown_links'], r'\1', text)
        # Remove markdown formatting characters (*bold*, _italic_, etc.)
        text = re.sub(self.reddit_patterns['markdown_formatting'], '', text)
        return text

    def remove_html(self, text: str) -> str:
        """
        Remove HTML tags and entities from text.
        
        Uses BeautifulSoup to parse and extract text content,
        then removes any remaining HTML entities.
        
        Args:
            text (str): Input text that may contain HTML
            
        Returns:
            str: Clean text with HTML removed
        """
        # Remove HTML tags using BeautifulSoup
        text = BeautifulSoup(text, 'html.parser').get_text()
        # Remove HTML entities (e.g., &amp;, &lt;, etc.)
        text = re.sub(self.reddit_patterns['html_entities'], ' ', text)
        return text

    def remove_deleted(self, text: str) -> str:
        """
        Remove Reddit's deleted/removed post indicators.
        
        Args:
            text (str): Input text that may contain deletion markers
            
        Returns:
            str: Text with deletion markers removed
        """
        return text.replace("[removed]", "").replace("[deleted]", "")

    def remove_emojis(self, text: str) -> str:
        """
        Remove emoji characters from text.
        
        Args:
            text (str): Input text that may contain emojis
            
        Returns:
            str: Text with emojis removed
        """
        return emoji.replace_emoji(text, '')

    def normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace characters in text.
        
        Replaces newlines, tabs, and multiple spaces with single spaces,
        then trims leading and trailing whitespace.
        
        Args:
            text (str): Input text with potentially irregular whitespace
            
        Returns:
            str: Text with normalized whitespace
        """
        # Replace newlines and tabs with spaces
        text = re.sub(r'[\n\t\r]+', ' ', text)
        # Remove multiple consecutive spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def normalize_unicode(self, text: str) -> str:
        """
        Normalize Unicode characters to ASCII where possible.
        
        Converts Unicode characters to their closest ASCII equivalents
        and removes characters that cannot be converted.
        
        Args:
            text (str): Input text with Unicode characters
            
        Returns:
            str: Text with Unicode normalized to ASCII
        """
        return unicode_normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

    def normalize_text(self, text: Optional[str]) -> str:
        """
        Main function to normalize Reddit submission text.
        
        Applies all normalization steps in sequence to produce clean,
        consistent text suitable for AI analysis. The process includes
        removing HTML, URLs, Reddit formatting, emojis, deleted content,
        Unicode normalization, and whitespace normalization.
        
        Args:
            text (Optional[str]): Input text to normalize
            lowercase (bool): Whether to convert text to lowercase (default: True)
            
        Returns:
            str: Fully normalized text string
            
        Note:
            If input text is None or empty, returns an empty string.
            The normalization process is designed to preserve meaningful
            content while removing formatting that could interfere with
            AI text analysis.
        """
        if not text:
            return ""

        text = str(text)

        text = self.remove_html(text)
        text = self.remove_urls(text)
        text = self.remove_reddit_formatting(text)
        text = self.remove_emojis(text)
        text = self.remove_deleted(text)
        text = self.normalize_unicode(text)
        text = self.normalize_whitespace(text)
        text = text.lower()

        return text
