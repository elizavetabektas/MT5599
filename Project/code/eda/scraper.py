"""Twitter Scraping Tool"""
import json
import snscrape.modules.twitter as sntwitter
from _datetime import datetime, timedelta
from multiprocessing import Pool
import tqdm # for progress bar
import pytz # for current time
import pandas as pd
import itertools

now = datetime.now().replace(tzinfo=pytz.utc)
start_date = (now - timedelta(days=365)).strftime('%Y-%m-%d')
end_date = (now + timedelta(days=1)).strftime('%Y-%m-%d')
date_window = str(start_date) + "-" + str(end_date)
path = "scaper_output.json"
scraper = sntwitter.TwitterSearchScraper


def get_tweetlist(handle: str):
    tweetlist = []
    for idx, tweet in enumerate(scraper(f'from:{handle} since:{start_date} until:{end_date}').get_items()):
        tweetlist.append({"id": str(tweet.id), "user": str(tweet.user.username), "DateTime": str(tweet.date), "tweet": str(tweet.content),
        "user_location": str(tweet.user.location),
        "place_fullname": str(tweet.place.fullName),
        "place_name": str(tweet.place.name),
        "place_type": str(tweet.place.type),
        "place_country": str(tweet.place.country),
        "place_countrycode": str(tweet.place.countryCode),
        "coordinates_longitude": str(tweet.coordinates.longitude),
        "coordinates_latitude": str(tweet.latitude)})

    print(f"{handle} completed!")
    return tweetlist

if __name__ == "__main__":
    with open('../data/argentina_users.txt') as f:
        handles = f.read().splitlines()
    handles = handles[0:1000]
    
    pool = Pool(processes=len(handles))
    results = []
    for result in tqdm.tqdm(pool.imap_unordered(get_tweetlist, handles), total=len(handles)):
        results.extend(result)

    with open("../data/argentinian_users_90days_2.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)