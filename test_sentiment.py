import json

from src.moodleguide.sentiment import (
    MultilingualSentimentAnalyzer
)


def main():
    analyzer = (
        MultilingualSentimentAnalyzer()
    )

    examples = [
        {
            "text": (
                "النظام ممتاز وساعدني "
                "في تسليم الواجب بسهولة"
            ),
            "language": "ar"
        },
        {
            "text": (
                "لا أستطيع فتح الاختبار "
                "وهذه المشكلة مزعجة جدا"
            ),
            "language": "ar"
        },
        {
            "text": (
                "متى يظهر المقرر "
                "في الصفحة الرئيسية؟"
            ),
            "language": "ar"
        },
        {
            "text": (
                "The Moodle system is "
                "easy to use and very helpful"
            ),
            "language": "en"
        },
        {
            "text": (
                "I cannot submit my assignment "
                "and I am very frustrated"
            ),
            "language": "en"
        },
        {
            "text": (
                "Where can I find my grades?"
            ),
            "language": "en"
        }
    ]

    for example in examples:
        result = analyzer.predict(
            text=example["text"],
            language=example["language"]
        )

        print("\n" + "=" * 60)
        print("Text:", example["text"])

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=4
            )
        )


if __name__ == "__main__":
    main()