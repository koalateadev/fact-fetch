from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer


def get_interesting_keywords(texts, top_n=10_000):
    """
    Extract interesting keywords using TF-IDF scores.
    
    This function uses TF-IDF (Term Frequency-Inverse Document Frequency) to identify
    the most important and distinctive keywords from a collection of text documents.
    It filters out common English stop words and focuses on terms that are most
    representative of the content.
    
    Args:
        texts (list): List of normalized strings from titles and descriptions
        top_n (int): The number of top keywords to extract globally from all texts (default: 10,000)
        
    Returns:
        list: List of top keywords ranked by TF-IDF importance
        
    Note:
        The function uses scikit-learn's TfidfVectorizer with English stop words
        removed to focus on meaningful content words rather than common function words.
    """
    # Initialize TF-IDF Vectorizer with English stop words removed
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)

    # Fit and transform texts to calculate TF-IDF scores
    vectorizer.fit_transform(texts)

    # Get feature names (keywords) ranked by importance
    feature_names = vectorizer.get_feature_names_out()

    return list(feature_names)


def cluster_keywords(keywords, num_clusters=100):
    """
    Cluster keywords into groups using embeddings and KMeans.
    
    This function uses sentence transformers to convert keywords into high-dimensional
    embeddings, then applies K-means clustering to group semantically similar keywords
    together. This helps identify topic clusters and related concepts.
    
    Args:
        keywords (list): List of keywords to cluster
        num_clusters (int): Number of clusters to create (default: 100)
        
    Returns:
        dict: A dictionary where the key is the cluster ID and the value is a list
              of keywords belonging to that cluster
              
    Note:
        The function uses the 'all-MiniLM-L6-v2' model for generating embeddings,
        which provides a good balance between performance and accuracy for keyword
        clustering tasks. K-means is used with a fixed random state for reproducible
        results.
    """
    # Load pre-trained embedding model for converting keywords to vectors
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate embeddings for the keywords
    embeddings = model.encode(keywords)

    # Perform K-means clustering on the embeddings
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    # Group keywords by their assigned cluster
    clusters = {}
    for keyword, label in zip(keywords, labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(keyword)

    return clusters