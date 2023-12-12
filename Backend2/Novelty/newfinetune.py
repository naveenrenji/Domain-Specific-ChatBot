import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, classification_report
from tqdm import tqdm

class NoveltyDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Load data
df = pd.read_csv('noveltyDataChatGPT.csv')
df['description'] = df['description'].fillna('missing').apply(lambda x: x.lower())

# Tokenize data
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

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
train_inputs, validation_inputs, train_labels, validation_labels = train_test_split(
    encoded_data['input_ids'],
    torch.tensor(df['novelty'].values),
    random_state=42,
    test_size=0.1
)

# Create Datasets
train_dataset = NoveltyDataset(
    {'input_ids': train_inputs, 'attention_mask': encoded_data['attention_mask'][:len(train_inputs)]},
    train_labels
)
validation_dataset = NoveltyDataset(
    {'input_ids': validation_inputs, 'attention_mask': encoded_data['attention_mask'][len(train_inputs):]},
    validation_labels
)

# Set up the training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=50,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    eval_steps=100,
    save_steps=100,
    logging_steps=100,
    evaluation_strategy='steps',
    save_total_limit=2,
    remove_unused_columns=False,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    greater_is_better=True,
    push_to_hub=False,
)

# Initialize the model
model = RobertaForSequenceClassification.from_pretrained('roberta-base')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(torch.cuda.is_available())
model = model.to(device)


def compute_metrics(p):
    return {"accuracy": accuracy_score(p.label_ids, p.predictions.argmax(-1))}

# Create the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=validation_dataset,
    compute_metrics=compute_metrics,
)

# Train the model
trainer.train()

# Save the fine-tuned model for later use
model.save_pretrained("./novelty_fine_tuned_model")
tokenizer.save_pretrained("./novelty_fine_tuned_model")

# Print Classification Report
predictions = trainer.predict(validation_dataset)
report = classification_report(predictions.label_ids, predictions.predictions.argmax(-1))
print(report)
