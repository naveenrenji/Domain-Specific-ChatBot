import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM, LineByLineTextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# 1. Specify main model, training and data arguments
model_name = 'distilbert-base-uncased'  # the model you want to fine-tune
output_dir = './model'  # where the fine-tuned model will be saved

# 2. Load pretrained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForMaskedLM.from_pretrained(model_name)

# 3. Load dataset
dataset = LineByLineTextDataset(
    tokenizer=tokenizer,
    file_path="dataset.txt",  # path to your dataset
    block_size=128,  # maximum sequence length
)

# 4. Specify data collator
# It will encode the data in a format that the model can understand and compute the loss
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

# 5. Initialize our Trainer
training_args = TrainingArguments(
    output_dir=output_dir,  # output directory for model predictions and checkpoints
    overwrite_output_dir=True,  # overwrite the content of the output directory
    num_train_epochs=3,  # number of training epochs
    per_device_train_batch_size=128,  # batch size for training
    save_steps=10_000,  # after # steps model is saved
    save_total_limit=2,  # delete other checkpoints and keep only the last 2
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

# 6. Train and save the model
trainer.train()
trainer.save_model(output_dir)
