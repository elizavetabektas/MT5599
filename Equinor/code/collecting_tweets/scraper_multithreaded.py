"""Twitter Scraping Tool"""
import json
import snscrape.modules.twitter as sntwitter
from _datetime import datetime, timedelta
from multiprocessing import Pool
import tqdm
import pytz

#def scrape():


now = datetime.now().replace(tzinfo=pytz.utc)
start_date = (now - timedelta(days=1)).strftime('%Y-%m-%d')
end_date = (now + timedelta(days=1)).strftime('%Y-%m-%d')
date_window = str(start_date) + "-" + str(end_date)
path = "scaper_output.json"
scraper = sntwitter.TwitterSearchScraper


def get_tweetlist(handle: str):
        tweetlist = []
        for idx, tweet in enumerate(scraper(f'from:{handle} since:{start_date} until:{end_date}').get_items()):
            if tweet.inReplyToTweetId is None:
                tweetlist.append({"id": str(tweet.id), "user": str(tweet.user.username), "DateTime": str(tweet.date),
                                  "tweet": str(tweet.content)})

        print(f"{handle} completed!")
        return tweetlist





if __name__ == "__main__":
    with open('Rubens_Twitter_handles') as f:
        handles = f.read().splitlines()
    pool = Pool(processes=len(handles))
    results = []
    for result in tqdm.tqdm(pool.imap_unordered(get_tweetlist, handles), total=len(handles)):
        results.extend(result)

    with open("../../data/daily_data/misc/date_window.txt", "w") as f:
        f.write(f"{start_date}-{now.strftime('%Y-%m-%d')}")
    with open("../../data/daily_data/misc/scraper_output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

