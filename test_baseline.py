import joblib

from src.moodleguide.preprocessing import preprocess_text


model = joblib.load(
    "models/baseline/topic_classifier.joblib"
)

examples = [
    {
        "text": "لا أستطيع تسليم ملف الواجب",
        "language": "ar"
    },
    {
        "text": "How can I create a quiz for my students?",
        "language": "en"
    },
    {
        "text": "المقرر غير ظاهر في حسابي",
        "language": "ar"
    },
    {
        "text": "My grade is not visible",
        "language": "en"
    }
]


for example in examples:
    processed_text = preprocess_text(
        example["text"],
        example["language"]
    )

    prediction = model.predict(
        [processed_text]
    )[0]

    probabilities = model.predict_proba(
        [processed_text]
    )[0]

    confidence = probabilities.max()

    print("-" * 50)
    print("Question:", example["text"])
    print("Predicted topic:", prediction)
    print("Confidence:", round(float(confidence), 4))