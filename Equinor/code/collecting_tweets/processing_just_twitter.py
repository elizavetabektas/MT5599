""""Data Processing Pipeline """
import re
import pandas as pd
import spacy
import py3langid as langid
import json
import unicodedata
import html


def process(s):
    r = unicodedata.normalize("NFC", s)
    r = html.unescape(r)
    r = r.encode("ascii", "ignore").decode()
    r = r.replace('\n', " ")
    r = r.replace('@', " ")
    r = r.replace("#", " ")
    r = re.sub('http://\S+|https://\S+', '', r)
    r = r.lower()
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    r = (emoji_pattern.sub(r'', r))  # no emoji
    r = re.sub('\s{2,}', ' ', r)
    return r

def format_datetime(df):
        df["DateTime"] = pd.to_datetime(df["DateTime"])
        df["DateTime"] = pd.DatetimeIndex(df["DateTime"]).floor('S').tz_localize(None)
        return df


def filter(text,nlp, blacklist, keywords):
        lemmas = [f"{token.lemma_}_{token.pos_}" for token in nlp(text)]
        tags = []
        for black in blacklist:
            if black in lemmas:
                return False
        for key in keywords.keys():
            if any(item in keywords[key] for item in lemmas):
                return True and len(text) >= 50 and langid.classify(text)[0] == 'en'

        return False

def get_processed_twitter_df(df, nlp):
    with open("./data/input_data/keywords_lemmatised.json", "r", encoding="utf-8") as f:
        keywords = json.load(f)
    with open("./data/input_data/blacklist.txt", "r", encoding="utf-8") as f:
        blacklist = f.readlines()
    keys = list(keywords.keys())
    print("ready for processing")
    df = format_datetime(df)
    tweets = df["tweet"]
    df["tweet"] = [process(x) for x in tweets]
    print("text formatted")
    df = df[[filter(x, nlp, blacklist, keywords) for x in tweets]]
    # lang_filter = (lambda text: langid.classify(text)[0] == 'en')
    #  df = df[[lang_filter(x) for x in tweets]]
    #  print("language filtered")
    #  df = df[[(len(x) >= 50) for x in tweets]]
    print("starting keyword filter")
    #   df = df[[filter(s) for s in df["tweet"]]]
    print("filtering complete")
   # df = df.reset_index()
    df.to_json("processing_output.json", indent=4)
    print("twitter processing finished")
    return df