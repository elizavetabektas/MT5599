# importing packages
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer
import hdbscan
import json

from topic_modelling.fitting_umap_hdbscan import extract_words_per_class

def infer_topics(df):

    # getting new tweets
    #path_to_fresh_tweets = "../../data/daily_data/misc/twitter_dataset.json"
   # df = pd.read_json(path_to_fresh_tweets).sample(frac=0.2)
    new_tweets = list(df['tweet'])

    # loading models required to put new tweets into existing clusters
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    umap_model = pickle.load(open('./models/umap_model_wednesday.pkl', 'rb'))
    hdbscan_model = pickle.load(open('./models/hdbscan_model_wednesday.pkl', 'rb'))

    # creating embeddings
    new_tweets_embeddings = sentence_model.encode(new_tweets, show_progress_bar=False)
    # reducing dimensionality using umap
    new_tweets_umap_embeddings = umap_model.transform(new_tweets_embeddings)
    # predicting clusters of new tweets using hdbscan
    labels, membership_strengths = hdbscan.approximate_predict(hdbscan_model, new_tweets_umap_embeddings)

    # getting updated keywords per class 
    #extract_words_per_class_output = extract_words_per_class(labels, new_tweets)
    #labelled_fresh_tweets = extract_words_per_class_output[0]
    #updated_words_per_class = extract_words_per_class_output[1]
    df["topic"] = labels

   # with open('updated_words_per_class.json', 'w') as fp:
    #    json.dump(updated_words_per_class, fp)

    #labelled_fresh_tweets.to_json('new_tweets_labelled.json', indent=4, orient="records")

    return df


if __name__ == "__main__":
    df = pd.read_json("./data/monthly_data/rolling_topic_window.json")
    df = infer_topics(df)
    df.to_json("./data/monthly_data/rolling_topic_window.json")
