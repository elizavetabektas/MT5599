import json
import pandas as pd
import snscrape.modules.twitter as sntwitter
from _datetime import datetime, timedelta
from multiprocessing import Pool
import tqdm
import pytz
from scraper_multithreaded import get_tweetlist
from processing_just_twitter import get_processed_twitter_df


if __name__ =="__main__":
    now = datetime.now().replace(tzinfo=pytz.utc)
    start_date = (now - timedelta(days=1)).strftime('%Y-%m-%d')
    end_date = (now + timedelta(days=1)).strftime('%Y-%m-%d')
    today = str(datetime(now.year, now.month, now.day))

    scraper = sntwitter.TwitterSearchScraper

    with open('../data/input_data/Input_Twitter_handles') as f:
        handles = f.read().splitlines()

    with open('../../data/input_data/geopolitics_handles.txt') as f:
        handles.extend(f.read().splitlines())

    with open('./data/input_data/markets_handles') as f:
        handles.extend(f.read().splitlines())

    results = []
    pool = Pool(processes=len(handles))
    for result in tqdm.tqdm(pool.imap_unordered(get_tweetlist, handles), total=len(handles)):
        results.extend(result)
    pool.close()
    df = pd.DataFrame(results)
    df = get_processed_twitter_df(df)
    print("data processed")
    df.to_json(f"../data/daily_data/raw/{today}_raw.json", indent = 4, orient="records")
