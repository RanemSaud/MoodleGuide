from pathlib import Path
import json

import pandas as pd

from src.moodleguide.semantic_search import (
    MoodleSemanticSearch
)


TEST_FILE = Path(
    "data/test/frozen_test.csv"
)

REPORT_FOLDER = Path("reports")
REPORT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


def calculate_metrics(dataframe):
    return {
        "queries": int(len(dataframe)),
        "recall_at_1": round(
            float(
                dataframe["recall_at_1"].mean()
            ),
            4
        ),
        "recall_at_3": round(
            float(
                dataframe["recall_at_3"].mean()
            ),
            4
        ),
        "recall_at_5": round(
            float(
                dataframe["recall_at_5"].mean()
            ),
            4
        ),
        "recall_at_10": round(
            float(
                dataframe["recall_at_10"].mean()
            ),
            4
        ),
        "mrr_at_10": round(
            float(
                dataframe["reciprocal_rank"].mean()
            ),
            4
        )
    }


def main():
    if not TEST_FILE.exists():
        raise FileNotFoundError(
            f"Test file not found: {TEST_FILE}"
        )

    test_df = pd.read_csv(
        TEST_FILE
    )

    required_columns = [
        "text",
        "language",
        "user_role",
        "topic"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in test_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    print(
        "Loading semantic search engine..."
    )

    search_engine = (
        MoodleSemanticSearch()
    )

    evaluation_rows = []

    total_queries = len(test_df)

    for row_number, row in test_df.iterrows():
        query = row["text"]
        expected_topic = row["topic"]
        user_role = row["user_role"]

        results = search_engine.search(
            query=query,
            user_role=user_role,
            top_k=10
        )

        relevant_rank = None

        for rank, result in enumerate(
            results,
            start=1
        ):
            if (
                result["topic"]
                == expected_topic
            ):
                relevant_rank = rank
                break

        if relevant_rank is None:
            reciprocal_rank = 0.0
        else:
            reciprocal_rank = (
                1.0 / relevant_rank
            )

        top_result = (
            results[0]
            if results
            else None
        )

        evaluation_rows.append(
            {
                "query": query,
                "language": row["language"],
                "user_role": user_role,
                "expected_topic": (
                    expected_topic
                ),
                "relevant_rank": (
                    relevant_rank
                    if relevant_rank is not None
                    else 0
                ),
                "recall_at_1": int(
                    relevant_rank is not None
                    and relevant_rank <= 1
                ),
                "recall_at_3": int(
                    relevant_rank is not None
                    and relevant_rank <= 3
                ),
                "recall_at_5": int(
                    relevant_rank is not None
                    and relevant_rank <= 5
                ),
                "recall_at_10": int(
                    relevant_rank is not None
                    and relevant_rank <= 10
                ),
                "reciprocal_rank": round(
                    reciprocal_rank,
                    4
                ),
                "top_result_topic": (
                    top_result["topic"]
                    if top_result
                    else None
                ),
                "top_result_question": (
                    top_result["question"]
                    if top_result
                    else None
                ),
                "top_result_score": (
                    top_result["score"]
                    if top_result
                    else 0.0
                )
            }
        )

        print(
            f"Query {row_number + 1}"
            f"/{total_queries} completed"
        )

    evaluation_df = pd.DataFrame(
        evaluation_rows
    )

    overall_metrics = calculate_metrics(
        evaluation_df
    )

    language_slices = {}

    for language, group in (
        evaluation_df.groupby("language")
    ):
        language_slices[
            str(language)
        ] = calculate_metrics(group)

    role_slices = {}

    for role, group in (
        evaluation_df.groupby("user_role")
    ):
        role_slices[
            str(role)
        ] = calculate_metrics(group)

    topic_slices = {}

    for topic, group in (
        evaluation_df.groupby(
            "expected_topic"
        )
    ):
        topic_slices[
            str(topic)
        ] = calculate_metrics(group)

    final_report = {
        "evaluation": (
            "semantic_search"
        ),
        "relevance_definition": (
            "A result is relevant when "
            "its topic matches the "
            "expected query topic."
        ),
        "overall": overall_metrics,
        "language_slices": (
            language_slices
        ),
        "role_slices": role_slices,
        "topic_slices": topic_slices
    }

    predictions_file = (
        REPORT_FOLDER
        / "semantic_search_predictions.csv"
    )

    metrics_file = (
        REPORT_FOLDER
        / "semantic_search_metrics.json"
    )

    errors_file = (
        REPORT_FOLDER
        / "semantic_search_errors.csv"
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
            final_report,
            file,
            ensure_ascii=False,
            indent=4
        )

    errors_df = evaluation_df[
        evaluation_df["recall_at_3"] == 0
    ]

    errors_df.to_csv(
        errors_file,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nSemantic search evaluation")
    print(
        "Queries:",
        overall_metrics["queries"]
    )
    print(
        "Recall@1:",
        overall_metrics["recall_at_1"]
    )
    print(
        "Recall@3:",
        overall_metrics["recall_at_3"]
    )
    print(
        "Recall@5:",
        overall_metrics["recall_at_5"]
    )
    print(
        "Recall@10:",
        overall_metrics["recall_at_10"]
    )
    print(
        "MRR@10:",
        overall_metrics["mrr_at_10"]
    )

    print("\nReports saved:")
    print(predictions_file)
    print(metrics_file)
    print(errors_file)


if __name__ == "__main__":
    main()