import json
import snscrape.modules.twitter as sntwitter
from multiprocessing import Pool
import tqdm
from collecting_tweets.scraper_multithreaded import get_tweetlist
from collecting_tweets.processing_just_twitter import get_processed_twitter_df
from nlp.NER import apply_ner
import pandas as pd
# from nlp.bertopic_inference import get_bertopic_inference
import os
from datetime import datetime, timedelta
import pytz
import spacy
from frontend.pre_frontend_processing import make_ner_dict, make_change_dict, make_topics_over_time, merge_json_files
import toml
#from nlp.hdbscan_topic_predictions import infer_topics


now = datetime.now().replace(tzinfo=pytz.utc)
start_date = (now - timedelta(days=1)).strftime('%Y-%m-%d')
end_date = (now + timedelta(days=1)).strftime('%Y-%m-%d')
today = str(datetime(now.year, now.month, now.day)).split(" ")[0]
"""Twitter Scraping"""
scraper = sntwitter.TwitterSearchScraper

toml_data = toml.load("./data/input_data/input.toml")
handles = []
for l in toml_data["handles"].values():
    handles.extend(l)

results = []
pool = Pool(processes=len(handles))
for result in tqdm.tqdm(pool.imap_unordered(get_tweetlist, handles), total=len(handles)):
    results.extend(result)
pool.close()
df = pd.DataFrame(results)

"""Data Processing"""
nlp = spacy.load("en_core_web_sm")
df = get_processed_twitter_df(df, nlp)
print("data processed")
df.to_json(f"./data/daily_data/raw/{today}_raw.json", indent=4, orient="records")

"""NLP Inference"""
df = apply_ner(df, nlp)
print("NER complete")

'''
df = infer_topics(df)
print("bertopic complete")
apath = "./data/labelled_df_wednesday.json"
all_data = pd.read_json(apath)
all_data = pd.concat([all_data, df], ignore_index=True).drop_duplicates(subset=['id'])
all_data.to_json(apath, indent=4, orient="records")
df.to_json(f"./data/daily_data/nlp/{today}_nlp.json", indent=4, orient="records")

print("new entries added")

"""Pre Frontend Processing"""
ners = df["ner"]
d = make_ner_dict(ners, nlp)
nerpath = os.path.join("./data/daily_data/ner_counts", str(today))
with open(nerpath + "_ner_counts.json", "w", encoding="UTF-8") as f:
    json.dump(d, f, indent=4)

def last_available_weekday(date):
    _offsets = (3, 1, 1, 1, 1, 1, 2)
    return date - timedelta(days=_offsets[date.weekday()])

with open(os.path.join("./data/daily_data/ner_counts", str(last_available_weekday(today))
                                                       + "_ner_counts.json")) as f:
    yesterdays_ners = json.load(f)

d2 = make_change_dict(d, yesterdays_ners)

with open(f"./data/daily_data/ner_changes/{today}_ner_changes.json", "w", encoding="UTF-8") as f:
    json.dump(d2, f, indent=4)

make_topics_over_time()
print("pre frontend complete")
'''