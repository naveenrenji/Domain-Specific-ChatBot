import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

def classify_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return 1 if model.config.id2label[predicted_class_id] == 'POSITIVE' else 0

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
        print(f"Response: {response} - Sentiment: {'Positive' if classify_sentiment(response) else 'Negative'}")

test_responses()
