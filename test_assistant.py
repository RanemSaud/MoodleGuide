import json

from src.moodleguide.assistant import (
    MoodleGuideAssistant
)


def main():
    assistant = MoodleGuideAssistant()

    questions = [
        {
            "text": "لا أستطيع رفع ملف الواجب",
            "language": "ar",
            "user_role": "student"
        },
        {
            "text": "كيف أنشئ اختبارا جديدا؟",
            "language": "ar",
            "user_role": "instructor"
        },
        {
            "text": "My course is missing",
            "language": "en",
            "user_role": "student"
        },
        {
            "text": "How do I publish grades?",
            "language": "en",
            "user_role": "instructor"
        }
    ]

    for question in questions:
        result = assistant.answer(
            text=question["text"],
            language=question["language"],
            user_role=question["user_role"]
        )

        print("\n" + "=" * 70)

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=4
            )
        )


if __name__ == "__main__":
    main()