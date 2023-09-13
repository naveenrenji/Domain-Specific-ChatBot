from transformers import BertTokenizer, BertForSequenceClassification
import torch
from os.path import dirname

def load_model():
    tokenizer = BertTokenizer.from_pretrained(f'{dirname(__file__)}/vftm/')
    model = BertForSequenceClassification.from_pretrained(f'{dirname(__file__)}/vftm/')
    return tokenizer, model

def predict_validation(description):
    tokenizer, model = load_model()
    model.eval()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    inputs = tokenizer(description, truncation=True, padding=True, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1)
    return 'yes' if prediction.item() == 1 else 'no'

# Example usage
#description = "have a washing machine that can detect if clothes have stains."
#print(f'Prediction for description:  {description} = {predict_validation(description)}')
