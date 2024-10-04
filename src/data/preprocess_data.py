import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from src import DIALOG_ACTS_FILE

bow_vocab = []
acts = [
        "negate", "affirm", "thankyou", "reqalts", "hello",
        "request", "restart", "repeat", "bye", "inform",
        "reqmore", "ack", "null", "deny", "confirm"
    ]
encoder = OneHotEncoder(categories=[list(range(len(acts)))], sparse_output=False)

def load_data(file_path=DIALOG_ACTS_FILE):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            dialog_act, utterance_content = line.strip().lower().split(" ", 1)
            data.append((dialog_act, utterance_content.strip()))
    return pd.DataFrame(data, columns = ['dialog_act', 'utterance_content'])

def preprocess_data(df):
    global bow_vocab

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['utterance_content'])
    y = df['dialog_act'].apply(lambda act: acts.index(act))

    bow_vocab = vectorizer.get_feature_names_out()

    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.15, random_state=42)

    train_y = encoder.fit_transform(train_y.values.reshape(-1, 1))
    test_y = encoder.transform(test_y.values.reshape(-1, 1))

    return train_x, train_y, test_x, test_y


df = load_data()
train_x, train_y, test_x, test_y = preprocess_data(df)

df_deduplicated = df.drop_duplicates(subset='utterance_content')
dtrain_x, dtrain_y, dtest_x, dtest_y = preprocess_data(df_deduplicated)
