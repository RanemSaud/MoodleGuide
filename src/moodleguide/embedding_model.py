import numpy as np
import torch
import torch.nn.functional as functional

from transformers import AutoModel, AutoTokenizer


class MultilingualEmbedder:

    def __init__(
        self,
        model_name,
        max_length=256
    ):
        self.model_name = model_name
        self.max_length = max_length

        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        print("Embedding device:", self.device)
        print("Loading embedding tokenizer...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        print("Loading embedding model...")

        self.model = AutoModel.from_pretrained(
            model_name
        )

        self.model.to(self.device)
        self.model.eval()

    @staticmethod
    def mean_pooling(
        token_embeddings,
        attention_mask
    ):
        expanded_mask = (
            attention_mask
            .unsqueeze(-1)
            .expand(token_embeddings.size())
            .float()
        )

        summed_embeddings = torch.sum(
            token_embeddings * expanded_mask,
            dim=1
        )

        summed_mask = torch.clamp(
            expanded_mask.sum(dim=1),
            min=1e-9
        )

        return summed_embeddings / summed_mask

    def encode(
        self,
        texts,
        batch_size=16,
        show_progress=True
    ):
        if isinstance(texts, str):
            texts = [texts]

        all_embeddings = []

        total_batches = (
            len(texts) + batch_size - 1
        ) // batch_size

        for start in range(
            0,
            len(texts),
            batch_size
        ):
            batch_texts = texts[
                start:start + batch_size
            ]

            encoded_inputs = self.tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt"
            )

            encoded_inputs = {
                key: value.to(self.device)
                for key, value in encoded_inputs.items()
            }

            with torch.no_grad():
                model_output = self.model(
                    **encoded_inputs
                )

            embeddings = self.mean_pooling(
                model_output.last_hidden_state,
                encoded_inputs["attention_mask"]
            )

            embeddings = functional.normalize(
                embeddings,
                p=2,
                dim=1
            )

            all_embeddings.append(
                embeddings.cpu().numpy()
            )

            if show_progress:
                batch_number = (
                    start // batch_size
                ) + 1

                print(
                    f"Encoding batch "
                    f"{batch_number}/{total_batches}"
                )

        return np.vstack(
            all_embeddings
        ).astype("float32")