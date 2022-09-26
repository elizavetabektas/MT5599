import pandas as pd
import spacy

def NER(data):
    from transformers import AutoTokenizer, AutoModelForTokenClassification
    from transformers import pipeline

    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-large-finetuned-conll03-english")
    model = AutoModelForTokenClassification.from_pretrained("xlm-roberta-large-finetuned-conll03-english")

    ner = pipeline("ner", model=model, tokenizer=tokenizer)
    data["ner"] = data["tweet"].apply(ner)
    return data


def ner(text):
        return {ent.text : ent.label_ for ent in nlp(text).ents}


def apply_ner(data, nlp):
    docs= [nlp(x) for x in data.tweet]
    out = [ner_join_MWEs(x) for x in docs]
    data["tweet_MWE"] = [x[0] for x in out]
    data["ner"] = [x[1] for x in out]

    return data


def ner_join_MWEs(spacy_doc):# -> tuple([str, list[tuple([str, str])]]):   # spacy_doc = nlp(s)
    #change the line token_ = token.lemma_.lower() to just token_ = token.text if the lemmas don’t help the clustering   
    final_text = list()
    ents = [ent for ent in spacy_doc.ents]
    ent_ix = [item for sublist in [[token.i for token in ent] for ent in ents]for item in sublist]
    for token in spacy_doc:
        token_ = token.lemma_.lower()
        if token.i in ent_ix:
            if token.i == 0:
                final_text.append([token_])
            else:
                if not isinstance(final_text[-1], list):
                    final_text.append([token_])
                else:
                    final_text[-1].append(token_)
        else:   
            final_text.append(token_)
    return (
        " ".join(
            ["_".join(item) if isinstance(item, list) else item for item in final_text]
        ),
        [tuple([ent.text, ent.label_]) for ent in ents],
    )




if __name__ == "__main__":
    df = pd.read_json("../../data/daily_data/misc/sentiment_output.json")
    df = NER2(df)
    df.to_json("ner2_output.json", indent = 4, orient="records")


    def NER3(text):
        doc = nlp(text)

    
