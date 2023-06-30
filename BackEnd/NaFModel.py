import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

# Load the dataset
df = pd.read_csv('data.csv')
dataset = Dataset.from_pandas(df)

# Split the dataset into train and test
dataset = dataset.train_test_split(test_size=0.2)

# Preprocess the dataset
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')

def preprocess_function(examples):
    return tokenizer(examples["description"], truncation=True, padding='max_length', max_length=512)

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Define the model
model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=5)

# Define the training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Define a function to compute metrics
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return {"accuracy": (predictions == labels).astype(np.float32).mean().item()}

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    eval_dataset=tokenized_dataset['test'],
    compute_metrics=compute_metrics,
)

# Train the model
trainer.train()

# Evaluate the model
trainer.evaluate()
