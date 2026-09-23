from pathlib import Path

import torch

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer
)

from .entity_extraction import MoodleEntityExtractor
from .preprocessing import preprocess_text
from .semantic_search import MoodleSemanticSearch
from .sentiment import MultilingualSentimentAnalyzer


class MoodleGuideAssistant:

    def __init__(
        self,
        classifier_path=(
            "models/transformer/topic_classifier"
        ),
        search_index_folder=(
            "models/semantic_search"
        )
    ):
        classifier_folder = Path(
            classifier_path
        )

        if not classifier_folder.exists():
            raise FileNotFoundError(
                "Transformer classifier was not found. "
                "Run train_transformer.py first."
            )

        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        print("Assistant device:", self.device)
        print("Loading topic classifier...")

        self.classifier_tokenizer = (
            AutoTokenizer.from_pretrained(
                classifier_path
            )
        )

        self.classifier_model = (
            AutoModelForSequenceClassification
            .from_pretrained(
                classifier_path
            )
        )

        self.classifier_model.to(
            self.device
        )

        self.classifier_model.eval()

        print("Loading semantic search...")

        self.search_engine = (
            MoodleSemanticSearch(
                index_folder=search_index_folder
            )
        )

        print("Loading sentiment analyzer...")

        self.sentiment_analyzer = (
            MultilingualSentimentAnalyzer()
        )

        print("Loading entity extractor...")

        self.entity_extractor = (
            MoodleEntityExtractor()
        )

        print("MoodleGuide assistant is ready")

    def predict_topic(
        self,
        text,
        language
    ):
        processed_text = preprocess_text(
            text,
            language
        )

        encoded_inputs = (
            self.classifier_tokenizer(
                processed_text,
                return_tensors="pt",
                truncation=True,
                max_length=128
            )
        )

        encoded_inputs = {
            key: value.to(self.device)
            for key, value
            in encoded_inputs.items()
        }

        with torch.no_grad():
            output = self.classifier_model(
                **encoded_inputs
            )

        probabilities = torch.softmax(
            output.logits,
            dim=-1
        )[0]

        predicted_id = int(
            torch.argmax(
                probabilities
            ).item()
        )

        topic = (
            self.classifier_model
            .config
            .id2label[predicted_id]
        )

        confidence = float(
            probabilities[predicted_id]
        )

        return {
            "processed_text": processed_text,
            "topic": topic,
            "confidence": round(
                confidence,
                4
            )
        }

    @staticmethod
    def determine_priority(
        sentiment,
        topic
    ):
        urgent_topics = {
            "quiz_exam",
            "login_access",
            "technical_problem"
        }

        if (
            sentiment == "negative"
            and topic in urgent_topics
        ):
            return "high"

        if sentiment == "negative":
            return "medium"

        return "normal"

    def answer(
        self,
        text,
        language,
        user_role
    ):
        text = str(text).strip()
        language = str(language).lower()
        user_role = str(user_role).lower()

        if not text:
            raise ValueError(
                "Question cannot be empty"
            )

        if language not in [
            "ar",
            "en"
        ]:
            raise ValueError(
                "Language must be ar or en"
            )

        if user_role not in [
            "student",
            "instructor"
        ]:
            raise ValueError(
                "User role must be "
                "student or instructor"
            )

        classification = self.predict_topic(
            text=text,
            language=language
        )

        sentiment_result = (
            self.sentiment_analyzer.predict(
                text=text,
                language=language
            )
        )

        entities = (
            self.entity_extractor.extract(
                text
            )
        )

        search_results = (
            self.search_engine.search(
                query=text,
                user_role=user_role,
                top_k=5
            )
        )

        final_topic = classification["topic"]
        topic_source = "classifier"

        if search_results:
            best_search_result = (
                search_results[0]
            )

            if (
                classification["confidence"] < 0.45
                and best_search_result["score"] >= 0.55
            ):
                final_topic = (
                    best_search_result["topic"]
                )

                topic_source = (
                    "semantic_search"
                )

        matching_topic_results = [
            result
            for result in search_results
            if result["topic"] == final_topic
        ]

        if matching_topic_results:
            selected_results = (
                matching_topic_results[:3]
            )
        else:
            selected_results = (
                search_results[:3]
            )

        if selected_results:
            best_result = selected_results[0]

            answer_text = (
                best_result["answer"]
            )

            route_to = (
                best_result["route_to"]
            )

            search_score = (
                best_result["score"]
            )

        else:
            answer_text = (
                "No suitable answer was found."
                if language == "en"
                else
                "لم يتم العثور على إجابة مناسبة."
            )

            route_to = (
                "eLearning Support"
            )

            search_score = 0.0

        priority = self.determine_priority(
            sentiment=(
                sentiment_result["sentiment"]
            ),
            topic=final_topic
        )

        similar_questions = [
            {
                "question": result["question"],
                "topic": result["topic"],
                "score": result["score"]
            }
            for result in selected_results
        ]

        return {
            "question": text,
            "language": language,
            "user_role": user_role,

            "predicted_topic": final_topic,
            "topic_source": topic_source,
            "classification_confidence": (
                classification["confidence"]
            ),

            "sentiment": (
                sentiment_result["sentiment"]
            ),
            "sentiment_confidence": (
                sentiment_result["confidence"]
            ),
            "sentiment_source": (
                sentiment_result["source"]
            ),
            "sentiment_scores": (
                sentiment_result["scores"]
            ),

            "entities": entities,

            "support_priority": priority,

            "answer": answer_text,
            "route_to": route_to,
            "search_score": search_score,

            "similar_questions": (
                similar_questions
            )
        }