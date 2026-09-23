from pathlib import Path
import inspect
import json
import numpy as np
import pandas as pd
import torch


from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
    set_seed
)


set_seed(42)

MODEL_NAME = "distilbert-base-multilingual-cased"
MAX_LENGTH = 128

train_file = Path("data/processed/splits/train.csv")
validation_file = Path("data/processed/splits/validation.csv")

output_folder = Path("models/transformer")
report_folder = Path("reports")

output_folder.mkdir(parents=True, exist_ok=True)
report_folder.mkdir(parents=True, exist_ok=True)


train_df = pd.read_csv(train_file)
validation_df = pd.read_csv(validation_file)

labels = sorted(train_df["topic"].unique())

label_to_id = {
    label: index
    for index, label in enumerate(labels)
}

id_to_label = {
    index: label
    for label, index in label_to_id.items()
}

print("Labels:")
print(label_to_id)

train_df["label"] = train_df["topic"].map(label_to_id)
validation_df["label"] = validation_df["topic"].map(label_to_id)


train_dataset = Dataset.from_pandas(
    train_df[["text", "label"]],
    preserve_index=False
)

validation_dataset = Dataset.from_pandas(
    validation_df[["text", "label"]],
    preserve_index=False
)


print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)


def tokenize_batch(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        max_length=MAX_LENGTH
    )


train_dataset = train_dataset.map(
    tokenize_batch,
    batched=True
)

validation_dataset = validation_dataset.map(
    tokenize_batch,
    batched=True
)

data_collator = DataCollatorWithPadding(
    tokenizer=tokenizer
)


print("Loading model...")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(labels),
    id2label=id_to_label,
    label2id=label_to_id
)


def compute_metrics(evaluation_prediction):
    logits, true_labels = evaluation_prediction

    predictions = np.argmax(
        logits,
        axis=-1
    )

    return {
        "accuracy": accuracy_score(
            true_labels,
            predictions
        ),
        "macro_f1": f1_score(
            true_labels,
            predictions,
            average="macro",
            zero_division=0
        )
    }


training_parameters = {
    "output_dir": str(output_folder / "checkpoints"),
    "num_train_epochs": 5,
    "learning_rate": 2e-5,
    "per_device_train_batch_size": 8,
    "per_device_eval_batch_size": 8,
    "weight_decay": 0.01,
    "warmup_steps": 10,
    "logging_steps": 10,
    "save_strategy": "epoch",
    "load_best_model_at_end": True,
    "metric_for_best_model": "macro_f1",
    "greater_is_better": True,
    "save_total_limit": 2,
    "report_to": "none",
    "seed": 42,
    "data_seed": 42,
    "fp16": torch.cuda.is_available()
}

# Supports both newer and older Transformers versions.
training_arguments_signature = inspect.signature(
    TrainingArguments.__init__
)

if "eval_strategy" in training_arguments_signature.parameters:
    training_parameters["eval_strategy"] = "epoch"
else:
    training_parameters["evaluation_strategy"] = "epoch"

training_args = TrainingArguments(
    **training_parameters
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=validation_dataset,
    processing_class=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    callbacks=[
        EarlyStoppingCallback(
            early_stopping_patience=2
        )
    ]
)


print("\nStarting Transformer training...")
print("GPU available:", torch.cuda.is_available())

trainer.train()

validation_results = trainer.evaluate()

print("\nValidation results:")
print(validation_results)


final_model_folder = output_folder / "topic_classifier"

trainer.save_model(final_model_folder)
tokenizer.save_pretrained(final_model_folder)

with open(
    final_model_folder / "label_mapping.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        {
            "label_to_id": label_to_id,
            "id_to_label": id_to_label
        },
        file,
        ensure_ascii=False,
        indent=4
    )

with open(
    report_folder / "transformer_validation_metrics.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        {
            key: float(value)
            for key, value in validation_results.items()
            if isinstance(value, (int, float))
        },
        file,
        ensure_ascii=False,
        indent=4
    )

print("\nModel saved:")
print(final_model_folder)