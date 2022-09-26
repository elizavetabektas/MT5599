# importing packages
import numpy as np
import pandas as pd
import transformers
import datasets
import sentence_transformers
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
import hdbscan
import json
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from bertopic._ctfidf import ClassTFIDF


def create_embeddings(sentence_model_name: str, df):
    """
    Creating embeddings for tweets using sentence transformers model
    """

    sentence_model = SentenceTransformer(sentence_model_name)
    tweets = list(df["tweet_MWE"])
    embeddings = sentence_model.encode(tweets, show_progress_bar=True)
    return embeddings


def save_embeddings(embeddings):
    np.save('embeddings.npy', embeddings)


def load_embeddings():
    embeddings = np.load('embeddings.npy')
    return embeddings


def reduce_dimensionality(embeddings,
                          n_neighbors: int,
                          n_components: int,
                          min_dist: float,
                          metric: str):
    """
    Reducing dimensionality of embeddings using UMAP
    """

    umap_model = umap.UMAP(n_neighbors=n_neighbors,
                           n_components=n_components,
                           min_dist=min_dist,
                           metric=metric,
                           low_memory=False)

    umap_embeddings = umap_model.fit_transform(embeddings)

    return umap_model, umap_embeddings


def cluster_embeddings(min_cluster_size: int,
                       min_samples: int,
                       metric: str,
                       cluster_selection_method: str,
                       umap_embeddings):
    """
    Clustering reduced dimension embeddings using density-based clustering HDBSCAN
    """

    hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size,
                                    min_samples=min_samples,
                                    metric=metric,
                                    cluster_selection_method=cluster_selection_method,
                                    prediction_data=True)

    clusters = hdbscan_model.fit(umap_embeddings)

    return hdbscan_model


def get_labels(hdbscan_model, df):
    labels = hdbscan_model.labels_.tolist()
    tweets = list(df["tweet"])
    return labels, tweets


def extract_words_per_class(labels, tweets):
    """
    Creating keyword lists for each topic using c-TF-IDF
    """
    # Label existing tweets
    labelled_tweets_array = np.array([tweets, labels]).T
    labelled_tweets_df = pd.DataFrame(labelled_tweets_array, columns=['Tweet', 'Numerical Label'])

    # Get data
    docs = pd.DataFrame({'Document': labelled_tweets_df.Tweet, 'Class': labelled_tweets_df['Numerical Label']})
    docs_per_class = docs.groupby(['Class'], as_index=False).agg({'Document': ' '.join})

    # Create bag of words
    count_vectorizer = CountVectorizer(stop_words='english').fit(docs_per_class.Document)
    count = count_vectorizer.transform(docs_per_class.Document)
    words = count_vectorizer.get_feature_names()

    # Extract top 20 words
    ctfidf_inst = ClassTFIDF()
    ctfidf_transformer = ctfidf_inst.fit(X=count)
    ctfidf = ctfidf_transformer.transform(count).toarray()
    words_per_class = {label: [words[index] for index in ctfidf[int(label) + 1].argsort()[-20:]] for label in
                       docs_per_class.Class}

    return labelled_tweets_df, words_per_class

if __name__ == "__main__":
    path_to_tweets_data = "../data/all_data.json"
    df = pd.read_json(path_to_tweets_data)

    embeddings = create_embeddings(sentence_model_name="all-mpnet-base-v2", df=df)

    umap_model, umap_embeddings = reduce_dimensionality(embeddings=embeddings, n_neighbors=4, n_components=2, min_dist=0.0,
                                                   metric='cosine')

    hdbscan_model = cluster_embeddings(min_cluster_size=int(df.shape[0] / 120), min_samples=int(df.shape[0] / 320),
                                       metric='euclidean', cluster_selection_method='eom',
                                       umap_embeddings=umap_embeddings)

    labels, tweets = get_labels(hdbscan_model, df)

    labelled_tweets_df, words_per_class = extract_words_per_class(labels, tweets)

    with open('../data/monthly_data/words_per_class_umap_hdbscan.json', 'w') as fp:
        json.dump(words_per_class, fp)

    labelled_tweets_df.to_csv('labelled_tweets_umap_hdbscan.csv', index=False)

    pickle.dump(umap_model, open('../models/umap_model.pkl', 'wb'))
    pickle.dump(hdbscan_model, open('../models/hdbscan_model.pkl', 'wb'))

