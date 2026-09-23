from pathlib import Path
import random
import pandas as pd


random.seed(42)

input_file = Path(
    "data/processed/moodle_inquiries_processed.csv"
)

output_file = Path(
    "data/processed/moodle_inquiries_expanded.csv"
)


arabic_prefixes = [
    "",
    "السلام عليكم، ",
    "لو سمحت، ",
    "احتاج مساعدة، ",
    "عندي استفسار، ",
    "ممكن توضيح، "
]

arabic_suffixes = [
    "",
    " وشكرا",
    " في نظام مودل",
    " ممكن تساعدوني؟",
    " ما الحل؟"
]

english_prefixes = [
    "",
    "Hello, ",
    "Please help, ",
    "I need help. ",
    "I have a question. ",
    "Could you explain? "
]

english_suffixes = [
    "",
    " Thank you.",
    " in Moodle.",
    " Could you help me?",
    " What should I do?"
]


def create_variation(text: str, language: str) -> str:
    if language == "ar":
        prefix = random.choice(arabic_prefixes)
        suffix = random.choice(arabic_suffixes)
    else:
        prefix = random.choice(english_prefixes)
        suffix = random.choice(english_suffixes)

    result = f"{prefix}{text.strip()}{suffix}"

    return " ".join(result.split())


df = pd.read_csv(input_file)

expanded_rows = []

variations_per_record = 20

for _, row in df.iterrows():
    created_texts = set()

    created_texts.add(row["processed_text"])

    attempts = 0

    while (
        len(created_texts) < variations_per_record
        and attempts < 200
    ):
        variation = create_variation(
            text=row["processed_text"],
            language=row["language"]
        )

        created_texts.add(variation)
        attempts += 1

    for text in created_texts:
        expanded_rows.append(
            {
                "source_id": row["id"],
                "text": text,
                "language": row["language"],
                "user_role": row["user_role"],
                "topic": row["topic"],
                "sentiment": row["sentiment"],
                "answer": row["answer"],
                "route_to": row["route_to"],
                "preprocessing_version":
                    row["preprocessing_version"]
            }
        )


expanded_df = pd.DataFrame(expanded_rows)

expanded_df.insert(
    0,
    "id",
    range(1, len(expanded_df) + 1)
)

expanded_df = expanded_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

expanded_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("Dataset expansion completed")
print("Original records:", len(df))
print("Expanded records:", len(expanded_df))
print("Output file:", output_file)

print("\nRecords by topic:")
print(expanded_df["topic"].value_counts())

print("\nRecords by role:")
print(expanded_df["user_role"].value_counts())

print("\nRecords by language:")
print(expanded_df["language"].value_counts())