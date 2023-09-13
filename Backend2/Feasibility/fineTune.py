import pandas as pd
import torch
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from tqdm import tqdm



# Load data
df = pd.read_csv('feasibilityDataChatGPT.csv')
df['description'] = df['description'].apply(lambda x: x.lower())

# Tokenize data
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
#tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")

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
    torch.tensor(df['feasibility'].values),
    encoded_data['attention_mask'],
    random_state=42,
    test_size=0.1
)

# Create Datasets
train_data = TensorDataset(train_inputs, train_masks, train_labels)
validation_data = TensorDataset(validation_inputs, validation_masks, validation_labels)

# Create Dataloaders
batch_size = 32
train_dataloader = DataLoader(train_data, batch_size=batch_size)
validation_dataloader = DataLoader(validation_data, batch_size=batch_size)

# Initialize the model
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
#model = AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions",num_labels=2)

# Optimizer
optimizer = AdamW(model.parameters(), lr=1e-5)

# Training loop
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

for epoch in range(3):
    model.train()
    total_loss = 0
    progress = tqdm(total=len(train_dataloader), desc='Epoch {:03d}'.format(epoch), ncols=80, leave=False)
    
    for step, batch in enumerate(train_dataloader):
        batch = tuple(t.to(device) for t in batch)
        inputs = {"input_ids": batch[0], "attention_mask": batch[1], "labels": batch[2]}
        outputs = model(**inputs)

        loss = outputs.loss
        loss.backward()
        total_loss += loss.item()
        
        optimizer.step()
        model.zero_grad()
        progress.update(1)
        progress.set_postfix({'loss': total_loss/(step+1)})


    avg_train_loss = total_loss / len(train_dataloader)
    tqdm.write(f"Train loss {avg_train_loss}")

    # Validation phase
    model.eval()
    predictions , true_labels = [], []
    for batch in validation_dataloader:
        input_ids, attention_mask, labels = tuple(t.to(device) for t in batch)
        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        predictions.extend(torch.argmax(logits, dim=-1).tolist())
        true_labels.extend(labels.tolist())
    logits = logits.detach().cpu().numpy()
    print(classification_report(true_labels, predictions))
    accuracy = accuracy_score(true_labels, predictions)  # Calculate the accuracy
    print("Accuracy:", accuracy)


    # Check if the accuracy is greater than 83% and save the model if so
    if accuracy > 0.85:
        print("Achieved desired accuracy. Saving and stopping training.")
        model.save_pretrained("./feasibility_fine_tuned_model")
        tokenizer.save_pretrained("./feasibility_fine_tuned_model")
        print("saved it")
        break  # Exit the training loop

# Save the fine-tuned model for later use
print("saving it")
model.save_pretrained("./feasibility_fine_tuned_model")
tokenizer.save_pretrained("./feasibility_fine_tuned_model")
print("saved it")