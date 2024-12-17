
import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TrainingArguments, Trainer
from sklearn.metrics import accuracy_score, f1_score
from datasets import Dataset
import pandas as pd

device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

model_dir = "./fine_tuned_model"

data = pd.read_csv("travel_intent.csv")
labels = list(set(data["Intent"]))
label_to_id = {label: i for i, label in enumerate(labels)}
id_to_label = {i: label for i, label in enumerate(labels)}

data["label"] = data["Intent"].map(label_to_id)
dataset = Dataset.from_pandas(data[["Query", "label"]])

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_function(examples):
    return tokenizer(examples["Query"], padding="longest", truncation=True)

tokenized_dataset = dataset.map(tokenize_function, batched=True)
train_test_split = tokenized_dataset.train_test_split(test_size=0.2)
train_dataset, eval_dataset = train_test_split["train"], train_test_split["test"]

if not os.path.exists(model_dir):
    model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(labels))
    model.to(device)

    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=64,
        gradient_accumulation_steps=2,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
    )

    def compute_metrics(pred):
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        return {
            "accuracy": accuracy_score(labels, preds),
            "f1": f1_score(labels, preds, average="weighted"),
        }

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics,
    )

    trainer.train()

    model.save_pretrained(model_dir)
    tokenizer.save_pretrained(model_dir)
    print("Model trained and saved.")
else:
    print("Model already trained. Skipping training.")

model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model.to(device)

def predict_intent(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=32).to(device)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_id = logits.argmax(-1).item()
    return id_to_label[predicted_class_id]

user_query = "I need a flight and hotel package to London."
predicted_intent = predict_intent(user_query)
print(f"Predicted Intent: {predicted_intent}")
