import os
import toml
if __name__ == "__main__":
    if not os.path.exists("../data"):
        os.mkdir("../data")
        os.mkdir("../data/daily_data")
        os.mkdir("../data/daily_data/ner_changes")
        os.mkdir("../data/daily_data/ner_counts")
        os.mkdir("../data/daily_data/nlp")
        os.mkdir("../data/daily_data/raw")
        os.mkdir("../data/monthly_data")
        os.mkdir("../data/input_data")
