# import the module
import tweepy
import os
import toml

if __name__ == "__main__":
    # assign the values accordingly
    consumer_key = "pjVwuCkqWjCoB8nkpW5HcM48H"
    consumer_secret = "FhtVwjYvwLbSqdSF7AYeF9ij2wkbmoOaZi5Wk5oEDmFvbzGlFi"
    access_token = "1542442029237653505-PQzl0Xx96fAqPWZwDLL3Pw8kPK3Rgp"
    access_token_secret = "8eayp7ZTrI35Azvy0ePFPX9l7NqHiqb5YbmJWQVq1youi"

    # fetching the members

    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # set access to user's access key and access secret
    auth.set_access_token(access_token, access_token_secret)

    # calling the api
    api = tweepy.API(auth)

    # the ID of the list
    geopolitics_list_id = '1254031884251774982'
    markets_list_id = '1254031533402402818'

    # fetching the members
    geopolitics_members = [str(x._json['screen_name']) for x in
                           api.get_list_members(list_id=geopolitics_list_id, count=500)]
    markets_members = [str(x._json['screen_name']) for x in api.get_list_members(list_id=markets_list_id, count=500)]

    # open file in write mode
    toml_path = "../data/input_data/input.toml"
    if not os.path.exists(toml_path):
        with open("../data/input_data/input_twitter_handles.txt", "r") as f:
            handles = list(f.read().splitlines())

        toml_data = {"handles": {"geopolitics_handles": geopolitics_members, "input_handles": handles,
                                 "markets_handles": markets_members, }}

        with open(toml_path, "w") as toml_file:
            toml.dump(toml_data, toml_file)

    else:
        toml_data = toml.load(toml_path)
        toml_data["handles"]["geopolitics_handles"] = geopolitics_members
        toml_data["handles"]["markets_handles"] = markets_members
        with open(toml_path, "w") as toml_file:
            toml.dump(toml_data, toml_file)
