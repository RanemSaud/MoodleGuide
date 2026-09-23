from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score
)


model = joblib.load(
    "models/baseline/topic_classifier.joblib"
)

test_df = pd.read_csv(
    "data/test/frozen_test.csv"
)

predictions = model.predict(
    test_df["processed_text"]
)

probabilities = model.predict_proba(
    test_df["processed_text"]
)

test_df["predicted_topic"] = predictions
test_df["confidence"] = probabilities.max(axis=1)

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

report = classification_report(
    test_df["topic"],
    predictions,
    output_dict=True,
    zero_division=0
)

labels = sorted(test_df["topic"].unique())

matrix = confusion_matrix(
    test_df["topic"],
    predictions,
    labels=labels
)

print("Frozen test results")
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


report_folder = Path("reports")
report_folder.mkdir(exist_ok=True)

results = {
    "model": "TF-IDF + Logistic Regression",
    "dataset": "frozen_test_v1",
    "records": len(test_df),
    "accuracy": round(accuracy, 4),
    "macro_f1": round(macro_f1, 4),
    "classification_report": report
}

with open(
    report_folder / "frozen_baseline_metrics.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        results,
        file,
        ensure_ascii=False,
        indent=4
    )


test_df.to_csv(
    report_folder / "frozen_baseline_predictions.csv",
    index=False,
    encoding="utf-8-sig"
)

matrix_df = pd.DataFrame(
    matrix,
    index=labels,
    columns=labels
)

matrix_df.to_csv(
    report_folder / "baseline_confusion_matrix.csv",
    encoding="utf-8-sig"
)


errors_df = test_df[
    test_df["topic"]
    != test_df["predicted_topic"]
]

errors_df.to_csv(
    report_folder / "frozen_baseline_errors.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nIncorrect predictions:", len(errors_df))
print("Reports saved in the reports folder")