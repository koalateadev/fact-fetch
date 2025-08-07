import sys

from fact_fetch.analysis.json_data_loader import load_json_line_by_line, get_x_results
from fact_fetch.analysis.keyword_extraction import get_interesting_keywords, cluster_keywords
from fact_fetch.utils.text_normalizer import RedditTextNormalizer


def main():
    text_normalizer = RedditTextNormalizer()

    filename = sys.argv[1]
    generator = load_json_line_by_line(filename)
    top_n = get_x_results(generator, 1000)
    normalized_strings = list(map(lambda x: text_normalizer.normalize_text(x['title'] + " " + x['selftext']), top_n))

    interesting_keywords = get_interesting_keywords(normalized_strings, top_n=100)
    clusters = cluster_keywords(interesting_keywords, num_clusters=10)

    print(clusters)

if __name__ == "__main__":
    main()