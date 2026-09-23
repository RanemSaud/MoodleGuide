import torch

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer
)

from .preprocessing import preprocess_text


class MultilingualSentimentAnalyzer:

    def __init__(
        self,
        model_name=(
            "lxyuan/"
            "distilbert-base-multilingual-cased-"
            "sentiments-student"
        )
    ):
        self.model_name = model_name

        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        print("Sentiment device:", self.device)
        print("Loading sentiment tokenizer...")

        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                self.model_name
            )
        )

        print("Loading sentiment model...")

        self.model = (
            AutoModelForSequenceClassification
            .from_pretrained(
                self.model_name
            )
        )

        self.model.to(self.device)
        self.model.eval()

    @staticmethod
    def normalize_label(label):
        label = str(label).lower()

        if "positive" in label:
            return "positive"

        if "negative" in label:
            return "negative"

        if "neutral" in label:
            return "neutral"

        return label

    @staticmethod
    def detect_domain_sentiment(text):
        text_lower = str(text).lower()

        negative_phrases = [
            "لا أستطيع",
            "لا استطيع",
            "لا يمكنني",
            "لا يمكن",
            "لا يعمل",
            "لا يفتح",
            "لا يظهر",
            "غير ظاهر",
            "لم يظهر",
            "مشكلة",
            "خطأ",
            "منزعج",
            "منزعجة",
            "تعطل",
            "متوقف",
            "اختفى",
            "فشل",
            "cannot",
            "can't",
            "can not",
            "does not work",
            "doesn't work",
            "not working",
            "not visible",
            "missing",
            "error",
            "problem",
            "failed",
            "frustrated"
        ]

        positive_phrases = [
            "ممتاز",
            "رائع",
            "شكرا",
            "شكرًا",
            "سهل",
            "سريعة",
            "سريع",
            "مفيد",
            "نجح",
            "excellent",
            "great",
            "helpful",
            "thank you",
            "thanks",
            "easy to use",
            "successful"
        ]

        for phrase in negative_phrases:
            if phrase in text_lower:
                return "negative"

        for phrase in positive_phrases:
            if phrase in text_lower:
                return "positive"

        return None

    def predict(
        self,
        text,
        language
    ):
        processed_text = preprocess_text(
            text,
            language
        )

        encoded_inputs = self.tokenizer(
            processed_text,
            return_tensors="pt",
            truncation=True,
            max_length=128
        )

        encoded_inputs = {
            key: value.to(self.device)
            for key, value
            in encoded_inputs.items()
        }

        with torch.no_grad():
            output = self.model(
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

        raw_label = (
            self.model
            .config
            .id2label[predicted_id]
        )

        model_sentiment = (
            self.normalize_label(
                raw_label
            )
        )

        model_confidence = float(
            probabilities[predicted_id]
        )

        all_scores = {}

        for label_id, score in enumerate(
            probabilities
        ):
            label = (
                self.model
                .config
                .id2label[label_id]
            )

            normalized_label = (
                self.normalize_label(label)
            )

            all_scores[normalized_label] = round(
                float(score),
                4
            )

        domain_sentiment = (
            self.detect_domain_sentiment(text)
        )

        if domain_sentiment is not None:
            final_sentiment = domain_sentiment
            sentiment_source = "domain_rule"
        else:
            final_sentiment = model_sentiment
            sentiment_source = "model"

        return {
            "sentiment": final_sentiment,
            "confidence": round(
                model_confidence,
                4
            ),
            "source": sentiment_source,
            "model_sentiment": model_sentiment,
            "scores": all_scores
        }