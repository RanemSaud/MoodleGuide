from pathlib import Path
import pandas as pd

from sklearn.model_selection import train_test_split


input_file = Path(
    "data/processed/moodle_inquiries_expanded.csv"
)

output_folder = Path("data/processed/splits")
output_folder.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_file)

# Combine topic and role to keep both balanced.
df["stratify_label"] = (
    df["topic"]
    + "_"
    + df["user_role"]
)

train_df, temporary_df = train_test_split(
    df,
    test_size=0.30,
    random_state=42,
    stratify=df["stratify_label"]
)

validation_df, test_df = train_test_split(
    temporary_df,
    test_size=0.50,
    random_state=42,
    stratify=temporary_df["stratify_label"]
)

columns_to_save = [
    column for column in df.columns
    if column != "stratify_label"
]

train_df[columns_to_save].to_csv(
    output_folder / "train.csv",
    index=False,
    encoding="utf-8-sig"
)

validation_df[columns_to_save].to_csv(
    output_folder / "validation.csv",
    index=False,
    encoding="utf-8-sig"
)

test_df[columns_to_save].to_csv(
    output_folder / "test.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Dataset split completed")
print("Training records:", len(train_df))
print("Validation records:", len(validation_df))
print("Testing records:", len(test_df))

print("\nTraining topic distribution:")
print(train_df["topic"].value_counts())