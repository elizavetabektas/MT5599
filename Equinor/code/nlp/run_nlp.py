from NER import apply_ner
import pandas as pd
from bertopic_inference import get_bertopic_inference
import os
from datetime import datetime, timedelta
import pytz
import spacy


if __name__ == "__main__":
    now = datetime.now().replace(tzinfo=pytz.utc) - timedelta(days=1)
    today = str(datetime(now.year, now.month, now.day))
    df = pd.read_json(f"./data/daily_data/raw/{today}_raw.json")
    nlp = spacy.load("en_core_web_sm")
    df = apply_ner(df, nlp)
    print("NER complete")
    apath = f"./data/all_data.json"
    if os.path.exists(apath):
        all_data = pd.read_json(apath).dropna()
        all_data = pd.concat([all_data, df], ignore_index=True).drop_duplicates(subset=['id'])
        all_data.to_json(apath, indent=4, orient="records")
    else:
        df.to_json(apath, indent=4, orient="records")

    df = get_bertopic_inference(df)
    print("bertopic complete")
    rpath = "./data/monthly_data/rolling_topic_window.json"

    if os.path.exists(rpath):
        all_data = pd.read_json(rpath).dropna()
        all_data = pd.concat([all_data, df], ignore_index=True).drop_duplicates(subset=['id'])
        all_data.to_json(rpath, indent=4, orient="records")
    else:
        df.to_json(rpath, indent=4, orient="records")

    outpath = os.path.join("./data/daily_data/nlp", f"{today}_nlp") + ".json"
    df.to_json(outpath, indent=4, orient="records")
    print("nlp complete")
