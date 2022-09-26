import pandas as pd
from datetime import datetime, timedelta
import spacy
import json
import os
import re

def merge_json_files(filename):
    result = list()
    for f1 in filename:
        with open(f1, 'r') as infile:
            result.extend(json.load(infile))
    with open('combined.json', 'w') as output_file:
        json.dump(result, output_file)


def value_comparison(x, y):
    try:
        return round(100 * (y - x) / x, 2)
    except ZeroDivisionError:
        return "inf"


def make_ner_dict(entity_list, spacy_model):
    ret = {label: {} for label in spacy_model.pipe_labels["ner"]}
    for entry in entity_list:
        for pair in list(entry):
            s = re.sub(r'[^\w\s]', '', pair[0])
            if s in ret[pair[1]]:
                ret[pair[1]][s] += 1
            else:
                ret[pair[1]].update({s: 1})
    return ret


def make_change_dict(today_dict, yesterday_dict):
    def make_key_dict(key, dict1, dict2):
        top_vals = dict(sorted(dict1[key].items(), key=lambda item: -item[1])[0:10])
        value_changes = []
        for loc in top_vals.items():
            try:
                yesterdays_value = dict2[key][loc[0]]
            except KeyError:
                yesterdays_value = 0
            value_changes.append(value_comparison(yesterdays_value, loc[1]))
        return {a: {"Quantity": b, "%Change": c} for a, b, c in
                zip(list(top_vals.keys()), top_vals.values(), value_changes)}

    return {key: make_key_dict(key, today_dict, yesterday_dict) for key in today_dict.keys()}


def make_topics_over_time():
    df3 = pd.read_json("./data/labelled_df_wednesday.json")
    df3["date"] = df3["DateTime"].apply(lambda dt: datetime(dt.year, dt.month, dt.day))
    df3 = df3[df3["topic"] != -1]
    df3 = df3[df3["DateTime"].apply(lambda x : x.weekday()<=4)]
    gb = df3.groupby(["date", "topic"]).size().to_frame().reset_index().rename(columns={0: "Frequency"})
    gb = gb.pivot(index='date', columns='topic').fillna(0)
    gb.Frequency.to_json("./data/topics_over_time2.json")
    gb.to_json(f"./data/topics_over_time.json", indent=4, orient="records")


if __name__ == "__main__":
  #  now = datetime.now() - timedelta(days=6)
  #  today = datetime(now.year, now.month, now.day)
   # inpath = os.path.join("./data/daily_data/nlp", str(today))
   ## df = pd.read_json(inpath + "_nlp.json")
   # print(df.columns)
   ## ners = df["ner"]
  #  nlp = spacy.load("en_core_web_sm")
  #  d = make_ner_dict(ners, nlp)

#    nerpath = os.path.join("./data/daily_data/ner_counts", str(today))
 #   with open(nerpath + "_ner_counts.json", "w", encoding="UTF-8") as f:
  #      json.dump(d, f, indent=4)

   # with open(os.path.join("./data/daily_data/ner_counts", str(today - timedelta(days=1)) + "_ner_counts.json")) as f:
    #    yesterdays_ners = json.load(f)

   # d2 = make_change_dict(d, yesterdays_ners)

#    with open(f"./data/daily_data/ner_changes/{today}_ner_changes.json", "w", encoding="UTF-8") as f:
 #       json.dump(d2, f, indent=4)

    make_topics_over_time()
