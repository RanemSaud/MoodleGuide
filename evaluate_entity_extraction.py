from pathlib import Path
import json

import pandas as pd

from src.moodleguide.entity_extraction import (
    MoodleEntityExtractor
)


TEST_FILE = Path(
    "data/test/entity_test.json"
)

REPORT_FOLDER = Path("reports")
REPORT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


def normalize_entity(entity):
    return (
        str(entity["type"]).strip().upper(),
        str(entity["value"]).strip().lower()
    )


def main():
    if not TEST_FILE.exists():
        raise FileNotFoundError(
            "Run create_entity_test.py first."
        )

    with open(
        TEST_FILE,
        encoding="utf-8"
    ) as file:
        test_cases = json.load(file)

    extractor = MoodleEntityExtractor()

    true_positive = 0
    false_positive = 0
    false_negative = 0

    evaluation_rows = []

    for case_number, test_case in enumerate(
        test_cases,
        start=1
    ):
        text = test_case["text"]

        expected = {
            normalize_entity(entity)
            for entity in (
                test_case["expected_entities"]
            )
        }

        predicted_entities = (
            extractor.extract(text)
        )

        predicted = {
            normalize_entity(entity)
            for entity in predicted_entities
        }

        correct = expected.intersection(
            predicted
        )

        extra = predicted.difference(
            expected
        )

        missing = expected.difference(
            predicted
        )

        true_positive += len(correct)
        false_positive += len(extra)
        false_negative += len(missing)

        evaluation_rows.append(
            {
                "case": case_number,
                "text": text,
                "expected": json.dumps(
                    sorted(expected),
                    ensure_ascii=False
                ),
                "predicted": json.dumps(
                    sorted(predicted),
                    ensure_ascii=False
                ),
                "correct": json.dumps(
                    sorted(correct),
                    ensure_ascii=False
                ),
                "extra": json.dumps(
                    sorted(extra),
                    ensure_ascii=False
                ),
                "missing": json.dumps(
                    sorted(missing),
                    ensure_ascii=False
                ),
                "exact_match": int(
                    expected == predicted
                )
            }
        )

    precision_denominator = (
        true_positive + false_positive
    )

    recall_denominator = (
        true_positive + false_negative
    )

    precision = (
        true_positive
        / precision_denominator
        if precision_denominator
        else 0.0
    )

    recall = (
        true_positive
        / recall_denominator
        if recall_denominator
        else 0.0
    )

    f1 = (
        2 * precision * recall
        / (precision + recall)
        if precision + recall
        else 0.0
    )

    evaluation_df = pd.DataFrame(
        evaluation_rows
    )

    exact_match_accuracy = float(
        evaluation_df["exact_match"].mean()
    )

    metrics = {
        "evaluation": (
            "rule_based_entity_extraction"
        ),
        "test_cases": len(test_cases),
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": round(
            precision,
            4
        ),
        "recall": round(
            recall,
            4
        ),
        "f1": round(
            f1,
            4
        ),
        "exact_match_accuracy": round(
            exact_match_accuracy,
            4
        )
    }

    predictions_file = (
        REPORT_FOLDER
        / "entity_predictions.csv"
    )

    metrics_file = (
        REPORT_FOLDER
        / "entity_metrics.json"
    )

    errors_file = (
        REPORT_FOLDER
        / "entity_errors.csv"
    )

    evaluation_df.to_csv(
        predictions_file,
        index=False,
        encoding="utf-8-sig"
    )

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

    errors_df = evaluation_df[
        evaluation_df["exact_match"] == 0
    ]

    errors_df.to_csv(
        errors_file,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nEntity extraction evaluation")
    print("Test cases:", len(test_cases))
    print("Precision:", round(precision, 4))
    print("Recall:", round(recall, 4))
    print("F1:", round(f1, 4))
    print(
        "Exact-match accuracy:",
        round(exact_match_accuracy, 4)
    )

    print("\nReports saved:")
    print(predictions_file)
    print(metrics_file)
    print(errors_file)


if __name__ == "__main__":
    main()