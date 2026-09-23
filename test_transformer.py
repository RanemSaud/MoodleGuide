import torch

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer
)

from src.moodleguide.preprocessing import preprocess_text


MODEL_PATH = "models/transformer/topic_classifier"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.eval()


def predict_topic(text: str, language: str):
    processed_text = preprocess_text(
        text,
        language
    )

    inputs = tokenizer(
        processed_text,
        return_tensors="pt",
        truncation=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(
        outputs.logits,
        dim=-1
    )[0]

    predicted_id = int(
        torch.argmax(probabilities).item()
    )

    return {
        "text": text,
        "topic": model.config.id2label[predicted_id],
        "confidence": round(
            float(probabilities[predicted_id]),
            4
        )
    }


examples = [
    ("لا أستطيع رفع ملف الواجب", "ar"),
    ("My course disappeared from Moodle", "en"),
    ("كيف أضيف اختبارًا جديدًا؟", "ar"),
    ("Students cannot view their grades", "en")
]


for text, language in examples:
    result = predict_topic(
        text,
        language
    )

    print("-" * 50)
    print(result)