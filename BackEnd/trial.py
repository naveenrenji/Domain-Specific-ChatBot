import pandas as pd
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModel, AdamW
from sklearn.metrics import classification_report
from tqdm import tqdm
import torch.nn as nn

def flat_accuracy(preds, labels):
    return np.sum(preds == labels) / len(labels)

# Load tokenizer and base model
tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
base_model = AutoModel.from_pretrained("SamLowe/roberta-base-go_emotions")

class NoveltyModel(nn.Module):
    def __init__(self, num_labels=2):  # Add num_labels parameter
        super(NoveltyModel, self).__init__()
        self.num_labels = num_labels  # Define num_labels attribute
        self.roberta = base_model
        self.out = nn.Linear(self.roberta.config.hidden_size, num_labels)  # Use num_labels here
    
    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.roberta(input_ids=input_ids, attention_mask=attention_mask)
        logits = self.out(outputs.pooler_output)
        loss_fct = nn.CrossEntropyLoss()  # Change to CrossEntropyLoss
        if labels is not None:
            labels = labels.long()  # Ensure labels are long integers
            loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))  # Remove the reshaping of labels
            return loss, logits
        return logits

# Load new model
model = NoveltyModel()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Define your optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

df = pd.read_csv('noveltyDataChatGPT.csv')
df['description'] = df['description'].apply(lambda x: x.lower())

# Convert the descriptions to list before passing to batch_encode_plus
descriptions = df['description'].values.tolist()
encoded_data = tokenizer.batch_encode_plus(
    descriptions, 
    add_special_tokens=True, 
    return_attention_mask=True,
    padding='max_length', 
    max_length=256, 
    return_tensors='pt'
)

# Split data into training and validation sets
train_inputs, validation_inputs, train_labels, validation_labels, train_masks, validation_masks = train_test_split(
    encoded_data['input_ids'],
    torch.tensor(df['novelty'].values),
    encoded_data['attention_mask'],
    random_state=42,
    test_size=0.1
)

# Create TensorDatasets
train_data = TensorDataset(train_inputs, train_masks, train_labels)
validation_data = TensorDataset(validation_inputs, validation_masks, validation_labels)

# Create DataLoaders
batch_size = 32
train_dataloader = DataLoader(train_data, shuffle=True, batch_size=batch_size)
validation_dataloader = DataLoader(validation_data, batch_size=batch_size)

# Training loop
for epoch in range(5):
    model.train()
    total_loss = 0
    progress = tqdm(total=len(train_dataloader), desc='Epoch {:03d}'.format(epoch), ncols=80, leave=False)
    
    for step, batch in enumerate(train_dataloader):
        batch = tuple(t.to(device) for t in batch)
        inputs = {"input_ids": batch[0], "attention_mask": batch[1], "labels": batch[2]}
        outputs = model(**inputs)

        loss = outputs[0]
        loss.backward()
        total_loss += loss.item()

        optimizer.step()
        model.zero_grad()
        progress.update(1)
        progress.set_postfix({'loss': total_loss/(step+1)})
    
    progress.close()

    # Validation phase
    model.eval()
    predictions , true_labels = [], []
    for batch in validation_dataloader:
        batch = tuple(t.to(device) for t in batch)
        inputs = {"input_ids": batch[0], "attention_mask": batch[1], "labels": batch[2]}
        with torch.no_grad():
            outputs = model(**inputs)
        
        logits = outputs[1]
        logits = logits.detach().cpu().numpy()
        label_ids = inputs["labels"].to('cpu').numpy()
        predictions.extend(np.argmax(logits, axis=1).flatten())
        true_labels.extend(label_ids.flatten())

    print(f"Validation Accuracy: {flat_accuracy(predictions, true_labels)}")


