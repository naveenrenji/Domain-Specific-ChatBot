from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax

def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def classify_sentiment(text):
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return np.argmax(scores)

def test_responses():
    responses = [
        "I'm doing great today!",
        "Today has been a rough day.",
        "Feeling wonderful this morning!",
        "It's been a mediocre day.",
        "Absolutely fantastic, thanks for asking!",
        "Not too good, honestly.",
        "Best day of my life!",
        "Could be better, honestly.",
        "I'm feeling awesome!",
        "It's a pretty bad day."
    ]
    for response in responses:
        score = classify_sentiment(response)
        print(f"Response: {response} - Sentiment Score: {score}")

test_responses()
