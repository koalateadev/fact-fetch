import sys

from fact_fetch.analysis.json_data_loader import load_json_line_by_line, get_x_results
from fact_fetch.analysis.keyword_extraction import get_interesting_keywords, cluster_keywords
from fact_fetch.utils.text_normalizer import RedditTextNormalizer


def main():
    """
    Main analysis function for processing Reddit submission data.
    
    This function performs keyword extraction and clustering analysis on Reddit posts.
    It loads JSON data from a file, normalizes the text content, extracts interesting
    keywords, and clusters them to identify common themes and topics.
    
    The analysis process:
    1. Loads Reddit submission data from a JSON file
    2. Normalizes text content using RedditTextNormalizer
    3. Extracts the most interesting keywords from the content
    4. Clusters keywords to identify topic groups
    5. Prints the clustering results
    
    Usage:
        python main.py <json_file_path>
        
    Args (via command line):
        json_file_path: Path to the JSON file containing Reddit submission data
        
    Note:
        The function processes the first 1000 submissions from the file
        and extracts the top 100 most interesting keywords, clustering
        them into 10 groups.
    """
    # Initialize text normalizer for cleaning Reddit content
    text_normalizer = RedditTextNormalizer()

    # Load data from command line argument
    filename = sys.argv[1]
    generator = load_json_line_by_line(filename)
    
    # Get the first 1000 submissions for analysis
    top_n = get_x_results(generator, 1000)
    
    # Normalize text content by combining title and body text
    normalized_strings = list(map(lambda x: text_normalizer.normalize_text(x['title'] + " " + x['selftext']), top_n))

    # Extract the most interesting keywords from the normalized content
    interesting_keywords = get_interesting_keywords(normalized_strings, top_n=100)
    
    # Cluster the keywords into topic groups
    clusters = cluster_keywords(interesting_keywords, num_clusters=10)

    # Print the clustering results
    print(clusters)


if __name__ == "__main__":
    main()