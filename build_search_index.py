from pathlib import Path
import json

import faiss
import pandas as pd

from src.moodleguide.embedding_model import (
    MultilingualEmbedder
)


MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)

DATA_FILE = Path(
    "data/raw/moodle_inquiries.csv"
)

OUTPUT_FOLDER = Path(
    "models/semantic_search"
)


def main():
    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    required_columns = [
        "id",
        "text",
        "language",
        "user_role",
        "topic",
        "answer",
        "route_to"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError(
            "The knowledge-base dataset is empty"
        )

    df["search_document"] = df.apply(
        lambda row: (
            f"language: {row['language']}. "
            f"role: {row['user_role']}. "
            f"topic: {row['topic']}. "
            f"question: {row['text']}. "
            f"answer: {row['answer']}"
        ),
        axis=1
    )

    embedding_model = MultilingualEmbedder(
        MODEL_NAME
    )

    print("Encoding knowledge base...")

    embeddings = embedding_model.encode(
        df["search_document"].tolist(),
        batch_size=16,
        show_progress=True
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(embeddings)

    index_file = (
        OUTPUT_FOLDER
        / "moodle_knowledge.index"
    )

    metadata_file = (
        OUTPUT_FOLDER
        / "metadata.csv"
    )

    manifest_file = (
        OUTPUT_FOLDER
        / "manifest.json"
    )

    faiss.write_index(
        index,
        str(index_file)
    )

    df.to_csv(
        metadata_file,
        index=False,
        encoding="utf-8-sig"
    )

    manifest = {
        "embedding_model": MODEL_NAME,
        "index_type": "IndexFlatIP",
        "pooling": "mean",
        "normalized_embeddings": True,
        "similarity": "cosine",
        "dimension": int(dimension),
        "documents": int(len(df))
    }

    with open(
        manifest_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            manifest,
            file,
            ensure_ascii=False,
            indent=4
        )

    print("\nSearch index created")
    print("Documents:", len(df))
    print("Embedding dimension:", dimension)
    print("Index entries:", index.ntotal)
    print("Index file:", index_file)
    print("Metadata file:", metadata_file)
    print("Manifest file:", manifest_file)


if __name__ == "__main__":
    main()