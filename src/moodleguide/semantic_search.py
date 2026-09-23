from pathlib import Path
import json

import faiss
import pandas as pd

from .embedding_model import (
    MultilingualEmbedder
)

class MoodleSemanticSearch:

    def __init__(
        self,
        index_folder="models/semantic_search"
    ):
        folder = Path(index_folder)

        manifest_file = (
            folder / "manifest.json"
        )

        index_file = (
            folder / "moodle_knowledge.index"
        )

        metadata_file = (
            folder / "metadata.csv"
        )

        if not manifest_file.exists():
            raise FileNotFoundError(
                "manifest.json was not found. "
                "Run build_search_index.py first."
            )

        if not index_file.exists():
            raise FileNotFoundError(
                "The FAISS index was not found. "
                "Run build_search_index.py first."
            )

        if not metadata_file.exists():
            raise FileNotFoundError(
                "metadata.csv was not found. "
                "Run build_search_index.py first."
            )

        with open(
            manifest_file,
            encoding="utf-8"
        ) as file:
            self.manifest = json.load(file)

        self.model = MultilingualEmbedder(
            self.manifest["embedding_model"]
        )

        self.index = faiss.read_index(
            str(index_file)
        )

        self.metadata = pd.read_csv(
            metadata_file
        )

        if self.index.ntotal != len(
            self.metadata
        ):
            raise ValueError(
                "The index and metadata "
                "contain different record counts."
            )

    def search(
        self,
        query,
        user_role=None,
        top_k=3
    ):
        query = str(query).strip()

        if not query:
            raise ValueError(
                "The search query cannot be empty"
            )

        if user_role:
            query_text = (
                f"role: {user_role}. "
                f"question: {query}"
            )
        else:
            query_text = (
                f"question: {query}"
            )

        query_embedding = self.model.encode(
            [query_text],
            batch_size=1,
            show_progress=False
        )

        search_size = min(
            max(top_k * 4, 10),
            self.index.ntotal
        )

        scores, indices = self.index.search(
            query_embedding,
            search_size
        )

        results = []

        for score, index_id in zip(
            scores[0],
            indices[0]
        ):
            if index_id < 0:
                continue

            row = self.metadata.iloc[
                int(index_id)
            ]

            if (
                user_role
                and row["user_role"]
                != user_role
            ):
                continue

            results.append(
                {
                    "score": round(
                        float(score),
                        4
                    ),
                    "question": row["text"],
                    "answer": row["answer"],
                    "topic": row["topic"],
                    "user_role": row["user_role"],
                    "language": row["language"],
                    "route_to": row["route_to"]
                }
            )

            if len(results) >= top_k:
                break

        return results