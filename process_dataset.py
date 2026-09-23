from pathlib import Path
import pandas as pd

from src.moodleguide.preprocessing import (
    PREPROCESSING_VERSION,
    preprocess_text
)


input_file = Path("data/raw/moodle_inquiries.csv")
output_folder = Path("data/processed")
output_file = output_folder / "moodle_inquiries_processed.csv"

output_folder.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_file)

required_columns = [
    "id",
    "text",
    "language",
    "user_role",
    "topic",
    "sentiment",
    "answer",
    "route_to"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )

df["processed_text"] = df.apply(
    lambda row: preprocess_text(
        text=row["text"],
        language=row["language"]
    ),
    axis=1
)

df["preprocessing_version"] = PREPROCESSING_VERSION

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("Dataset processed successfully")
print("Input records:", len(df))
print("Output file:", output_file)

print("\nPreview:")
print(
    df[
        [
            "text",
            "processed_text",
            "language",
            "user_role",
            "topic"
        ]
    ].head()
)