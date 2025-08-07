from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer


def get_interesting_keywords(texts, top_n=1000):
    """
    Extract interesting keywords using TF-IDF scores.
    Args:
        texts (list): List of normalized strings from titles and descriptions.
        top_n (int): The number of top keywords to extract globally from all texts.

    Returns:
        list: List of top keywords.
    """
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)

    # Fit and transform texts
    vectorizer.fit_transform(texts)

    # Get feature names (keywords)
    feature_names = vectorizer.get_feature_names_out()

    return list(feature_names)

def cluster_keywords(keywords, num_clusters=100):
    """
    Cluster keywords into groups using embeddings and KMeans.
    Args:
        keywords (list): List of keywords to cluster.
        num_clusters (int): Number of clusters.

    Returns:
        dict: A dictionary where the key is the cluster ID and the value is a list of keywords belonging to that cluster.
    """
    # Load pre-trained embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate embeddings for the keywords
    embeddings = model.encode(keywords)

    # Perform clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    # Group keywords by cluster
    clusters = {}
    for keyword, label in zip(keywords, labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(keyword)

    return clusters