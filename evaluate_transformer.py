from pathlib import Path
import json

import pandas as pd
import torch

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score
)

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer
)


MODEL_PATH = "models/transformer/topic_classifier"
TEST_FILE = "data/test/frozen_test.csv"

report_folder = Path("reports")
report_folder.mkdir(exist_ok=True)


device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print("Using device:", device)


tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.to(device)
model.eval()


test_df = pd.read_csv(TEST_FILE)

texts = test_df["processed_text"].tolist()

inputs = tokenizer(
    texts,
    padding=True,
    truncation=True,
    max_length=128,
    return_tensors="pt"
)

inputs = {
    key: value.to(device)
    for key, value in inputs.items()
}


with torch.no_grad():
    outputs = model(**inputs)

probabilities = torch.softmax(
    outputs.logits,
    dim=-1
)

predicted_ids = torch.argmax(
    probabilities,
    dim=-1
).cpu().tolist()

confidence_scores = torch.max(
    probabilities,
    dim=-1
).values.cpu().tolist()


predictions = [
    model.config.id2label[predicted_id]
    for predicted_id in predicted_ids
]


test_df["predicted_topic"] = predictions
test_df["confidence"] = [
    round(float(score), 4)
    for score in confidence_scores
]


accuracy = accuracy_score(
    test_df["topic"],
    predictions
)

macro_f1 = f1_score(
    test_df["topic"],
    predictions,
    average="macro",
    zero_division=0
)


print("\nTransformer frozen-test results")
print("Accuracy:", round(accuracy, 4))
print("Macro F1:", round(macro_f1, 4))

print("\nClassification report:")
print(
    classification_report(
        test_df["topic"],
        predictions,
        zero_division=0
    )
)


def calculate_slice_metrics(
    dataframe,
    column_name
):
    results = {}

    for value, group in dataframe.groupby(column_name):
        results[str(value)] = {
            "records": int(len(group)),
            "accuracy": round(
                accuracy_score(
                    group["topic"],
                    group["predicted_topic"]
                ),
                4
            ),
            "macro_f1": round(
                f1_score(
                    group["topic"],
                    group["predicted_topic"],
                    average="macro",
                    zero_division=0
                ),
                4
            )
        }

    return results


metrics = {
    "model": "distilbert-base-multilingual-cased",
    "dataset": "frozen_test_v1",
    "records": len(test_df),
    "accuracy": round(accuracy, 4),
    "macro_f1": round(macro_f1, 4),
    "language_slices": calculate_slice_metrics(
        test_df,
        "language"
    ),
    "role_slices": calculate_slice_metrics(
        test_df,
        "user_role"
    ),
    "classification_report": classification_report(
        test_df["topic"],
        predictions,
        output_dict=True,
        zero_division=0
    )
}


with open(
    report_folder / "frozen_transformer_metrics.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        metrics,
        file,
        ensure_ascii=False,
        indent=4
    )


test_df.to_csv(
    report_folder / "frozen_transformer_predictions.csv",
    index=False,
    encoding="utf-8-sig"
)


errors_df = test_df[
    test_df["topic"]
    != test_df["predicted_topic"]
]

errors_df.to_csv(
    report_folder / "frozen_transformer_errors.csv",
    index=False,
    encoding="utf-8-sig"
)


labels = sorted(test_df["topic"].unique())

matrix = confusion_matrix(
    test_df["topic"],
    predictions,
    labels=labels
)

matrix_df = pd.DataFrame(
    matrix,
    index=labels,
    columns=labels
)

matrix_df.to_csv(
    report_folder / "transformer_confusion_matrix.csv",
    encoding="utf-8-sig"
)


print("\nIncorrect predictions:", len(errors_df))
print("Reports saved successfully")