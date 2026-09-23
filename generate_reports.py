from pathlib import Path
import json


REPORT_FOLDER = Path("reports")

REPORT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


def load_json(filename):
    file_path = REPORT_FOLDER / filename

    if not file_path.exists():
        print(
            f"File not found: {file_path}"
        )

        return None

    with open(
        file_path,
        encoding="utf-8"
    ) as file:
        return json.load(file)


def format_number(value):
    if value is None:
        return "Not available"

    if isinstance(value, float):
        return f"{value:.4f}"

    return str(value)


def main():
    baseline = load_json(
        "frozen_baseline_metrics.json"
    )

    transformer = load_json(
        "frozen_transformer_metrics.json"
    )

    semantic_search = load_json(
        "semantic_search_metrics.json"
    )

    entities = load_json(
        "entity_metrics.json"
    )

    benchmark = load_json(
        "api_benchmark.json"
    )

    print("\nFiles reading completed")

    print(
        "Baseline results:",
        "Found" if baseline else "Not found"
    )

    print(
        "Transformer results:",
        "Found" if transformer else "Not found"
    )

    print(
        "Semantic-search results:",
        "Found" if semantic_search else "Not found"
    )

    print(
        "Entity results:",
        "Found" if entities else "Not found"
    )

    print(
        "Benchmark results:",
        "Found" if benchmark else "Not found"
    )

    baseline_accuracy = (
        baseline.get("accuracy")
        if baseline
        else None
    )

    baseline_f1 = (
        baseline.get("macro_f1")
        if baseline
        else None
    )

    transformer_accuracy = (
        transformer.get("accuracy")
        if transformer
        else None
    )

    transformer_f1 = (
        transformer.get("macro_f1")
        if transformer
        else None
    )

    search_results = (
        semantic_search.get(
            "overall",
            {}
        )
        if semantic_search
        else {}
    )

    recall_at_1 = (
        search_results.get(
            "recall_at_1"
        )
    )

    recall_at_3 = (
        search_results.get(
            "recall_at_3"
        )
    )

    recall_at_10 = (
        search_results.get(
            "recall_at_10"
        )
    )

    mrr_at_10 = (
        search_results.get(
            "mrr_at_10"
        )
    )

    entity_precision = (
        entities.get("precision")
        if entities
        else None
    )

    entity_recall = (
        entities.get("recall")
        if entities
        else None
    )

    entity_f1 = (
        entities.get("f1")
        if entities
        else None
    )

    entity_exact_match = (
        entities.get(
            "exact_match_accuracy"
        )
        if entities
        else None
    )

    benchmark_latency = (
        benchmark.get(
            "latency_ms",
            {}
        )
        if benchmark
        else {}
    )

    successful_requests = (
        benchmark.get(
            "successful_requests"
        )
        if benchmark
        else None
    )

    throughput = (
        benchmark.get(
            "throughput_requests_per_second"
        )
        if benchmark
        else None
    )

    mean_latency = (
        benchmark_latency.get("mean")
    )

    p50_latency = (
        benchmark_latency.get("p50")
    )

    p95_latency = (
        benchmark_latency.get("p95")
    )

    p99_latency = (
        benchmark_latency.get("p99")
    )

    evaluation_report = f"""# MoodleGuide Evaluation Report

## Project Overview

MoodleGuide is a bilingual intelligent academic assistant for Moodle LMS.

The system supports Arabic and English questions from students and instructors.

## Topic Classification Results

| Model | Accuracy | Macro F1 |
|---|---:|---:|
| TF-IDF and Logistic Regression | {format_number(baseline_accuracy)} | {format_number(baseline_f1)} |
| Multilingual DistilBERT | {format_number(transformer_accuracy)} | {format_number(transformer_f1)} |

## Semantic Search Results

| Metric | Result |
|---|---:|
| Recall@1 | {format_number(recall_at_1)} |
| Recall@3 | {format_number(recall_at_3)} |
| Recall@10 | {format_number(recall_at_10)} |
| MRR@10 | {format_number(mrr_at_10)} |


## Notes

The TF-IDF model is the baseline model.

Multilingual DistilBERT is the Transformer model.

The frozen test dataset was not used during training.
"""

    evaluation_file = (
        REPORT_FOLDER
        / "EVALUATION_REPORT.md"
    )

    evaluation_file.write_text(
        evaluation_report,
        encoding="utf-8"
    )

    print(
        "\nEvaluation report created:"
    )

    print(evaluation_file)


if __name__ == "__main__":
    main()