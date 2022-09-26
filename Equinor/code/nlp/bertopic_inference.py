from bertopic import BERTopic

def get_bertopic_inference(df):
    model = BERTopic.load("./models/bertopic_model")
    print("bertopic ready")
    print("Classifying!")
    tweets = df["tweet"].tolist()
    df["topic"] = model.transform(tweets)[0]
    return df



