# classify_with_saved_model.py

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from os.path import dirname

# Load the fine-tuned model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(f'{dirname(__file__)}/fftm/')
model = AutoModelForSequenceClassification.from_pretrained(f'{dirname(__file__)}/fftm/')

# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Function to classify a text
def classify_feasibility(text):
    model.eval()
    inputs = tokenizer.encode_plus(
        text.lower(),
        add_special_tokens=True,
        return_attention_mask=True,
        padding='max_length', 
        max_length=256, 
        return_tensors='pt'
    )

    input_ids = inputs['input_ids'].to(device)
    with torch.no_grad():
        outputs = model(input_ids)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return probs[0][1].item()

# # Prompting user input
# while True:
#     user_input = input("Please enter a description (or 'stop' to quit): ")
    
#     if user_input.lower() == 'stop':
#         break

#     feasibility_score = classify_text(user_input)
#     print(f'The feasibility score of your input is: {feasibility_score}')
