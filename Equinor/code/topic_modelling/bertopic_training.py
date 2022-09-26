# loading necessary packages
import pandas as pd
import transformers
import sentence_transformers
import umap.umap_
import hdbscan
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import json
from datetime import datetime, timedelta

import nltk
nltk.download('stopwords')

def get_stopwords():
    languages = stopwords.fileids()
    stopword_list = list()
    for language in languages:
        stopword_list += list(stopwords.words(language))
    return stopword_list

def instantiate_models(sentence_model_name:str,
                            n_neighbors:int,
                            n_components:int,
                            min_dist:float,
                            umap_metric:str,
                            min_cluster_size:int,
                            min_samples:int,
                            hdbscan_metric:str,
                            cluster_selection_method:str,
                            stopword_list,
                            top_n_words:int,
                            seed_topic_list,
                            bertopic_language:str):

    embedding_model = SentenceTransformer(sentence_model_name)

    umap_model = umap.umap_.UMAP(n_neighbors=n_neighbors,
                       n_components=n_components,
                       min_dist=min_dist,
                       metric=umap_metric, 
                       low_memory=False)

    hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size,
                                min_samples=min_samples,
                                metric=hdbscan_metric,
                                cluster_selection_method=cluster_selection_method,
                                prediction_data=True)

    vectorizer_model = CountVectorizer(stop_words=stopword_list)

    model = BERTopic(
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        embedding_model=embedding_model,
        vectorizer_model=vectorizer_model,
        top_n_words=top_n_words,
        language=bertopic_language,
        calculate_probabilities=True,
        verbose=True,
        seed_topic_list = seed_topic_list,
    )

    return model

if __name__ == "__main__":
    path_to_tweets_data = "../../data/daily_data/misc/60_days_plus_MWEs.json"
    df = pd.read_json(path_to_tweets_data)
    lookback_limit = datetime.now() - timedelta(days=60)
    df = df[df["DateTime"] >= lookback_limit]

    tweets = list(df["tweet"])

    stopword_list = get_stopwords()

    with open('../../data/monthly_data/words_per_class_umap_hdbscan.json', 'r') as f:
        old_topics = json.load(f)

    seed_topic_list = []
    for i in old_topics:
        seed_topic_list += [old_topics[i]]    

    model = instantiate_models(sentence_model_name="all-mpnet-base-v2",
                            n_neighbors=4,
                            n_components=5,
                            min_dist=0.0,
                            umap_metric='cosine',
                            min_cluster_size=int(df.shape[0] / 20),
                            min_samples=int(df.shape[0] / 20),
                            hdbscan_metric='euclidean',
                            cluster_selection_method='eom',
                            stopword_list=stopword_list,
                            top_n_words=20,
                            seed_topic_list=seed_topic_list,
                            bertopic_language='english')

    topics, probs = model.fit_transform(tweets)
    print(f"Num topics: {len(model.topics)}")
    model.save('../models/bertopic_model')
    with open("../data/monthly_data/topic_keywords.json", "w", encoding="UTF-8") as f:
        json.dump(model.topics, f)

    df["topic"] = topics
    df.to_json("../data/rolling_topic_window.json", indent=4, orient="records")
    




