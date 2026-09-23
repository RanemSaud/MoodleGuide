from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score
)
from sklearn.pipeline import Pipeline


train_file = Path("data/processed/splits/train.csv")
validation_file = Path("data/processed/splits/validation.csv")
test_file = Path("data/processed/splits/test.csv")

model_folder = Path("models/baseline")
report_folder = Path("reports")

model_folder.mkdir(parents=True, exist_ok=True)
report_folder.mkdir(parents=True, exist_ok=True)


train_df = pd.read_csv(train_file)
validation_df = pd.read_csv(validation_file)
test_df = pd.read_csv(test_file)

print("Training records:", len(train_df))
print("Validation records:", len(validation_df))
print("Testing records:", len(test_df))


model = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(3, 5),
                min_df=2,
                max_features=20000,
                sublinear_tf=True
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                random_state=42
            )
        )
    ]
)


print("\nTraining baseline model...")

model.fit(
    train_df["text"],
    train_df["topic"]
)

print("Training completed")


validation_predictions = model.predict(
    validation_df["text"]
)

test_predictions = model.predict(
    test_df["text"]
)


validation_accuracy = accuracy_score(
    validation_df["topic"],
    validation_predictions
)

validation_macro_f1 = f1_score(
    validation_df["topic"],
    validation_predictions,
    average="macro"
)

test_accuracy = accuracy_score(
    test_df["topic"],
    test_predictions
)

test_macro_f1 = f1_score(
    test_df["topic"],
    test_predictions,
    average="macro"
)


print("\nValidation results")
print("Accuracy:", round(validation_accuracy, 4))
print("Macro F1:", round(validation_macro_f1, 4))

print("\nTest results")
print("Accuracy:", round(test_accuracy, 4))
print("Macro F1:", round(test_macro_f1, 4))

print("\nClassification report")
print(
    classification_report(
        test_df["topic"],
        test_predictions,
        zero_division=0
    )
)


def calculate_slice_metrics(
    dataframe,
    predictions,
    column_name
):
    slice_results = {}

    evaluation_df = dataframe.copy()
    evaluation_df["prediction"] = predictions

    for value, group in evaluation_df.groupby(column_name):
        slice_results[str(value)] = {
            "records": int(len(group)),
            "accuracy": round(
                accuracy_score(
                    group["topic"],
                    group["prediction"]
                ),
                4
            ),
            "macro_f1": round(
                f1_score(
                    group["topic"],
                    group["prediction"],
                    average="macro",
                    zero_division=0
                ),
                4
            )
        }

    return slice_results


metrics = {
    "model": "TF-IDF character n-grams + Logistic Regression",
    "validation": {
        "accuracy": round(validation_accuracy, 4),
        "macro_f1": round(validation_macro_f1, 4)
    },
    "test": {
        "accuracy": round(test_accuracy, 4),
        "macro_f1": round(test_macro_f1, 4)
    },
    "language_slices": calculate_slice_metrics(
        test_df,
        test_predictions,
        "language"
    ),
    "role_slices": calculate_slice_metrics(
        test_df,
        test_predictions,
        "user_role"
    )
}


metrics_file = report_folder / "baseline_metrics.json"

with open(
    metrics_file,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        metrics,
        file,
        ensure_ascii=False,
        indent=4
    )


errors_df = test_df.copy()
errors_df["predicted_topic"] = test_predictions

errors_df = errors_df[
    errors_df["topic"]
    != errors_df["predicted_topic"]
]

errors_df.to_csv(
    report_folder / "baseline_errors.csv",
    index=False,
    encoding="utf-8-sig"
)


joblib.dump(
    model,
    model_folder / "topic_classifier.joblib"
)


print("\nFiles saved:")
print(model_folder / "topic_classifier.joblib")
print(report_folder / "baseline_metrics.json")
print(report_folder / "baseline_errors.csv")