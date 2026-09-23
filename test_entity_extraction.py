import json

from src.moodleguide.entity_extraction import (
    MoodleEntityExtractor
)


def main():
    extractor = MoodleEntityExtractor()

    examples = [
        (
            "لا أستطيع رفع ملف PDF في الواجب الثالث "
            "لمقرر معالجة اللغة الطبيعية"
        ),
        (
            "يظهر خطأ 403 عند فتح الاختبار النهائي"
        ),
        (
            "موعد تسليم التكليف هو 25/09/2026"
        ),
        (
            "My student ID is 2026123456 and "
            "I cannot open Quiz 2"
        ),
        (
            "How do I upload a PPTX file "
            "to the Python course?"
        ),
        (
            "درجات مقرر الذكاء الاصطناعي غير ظاهرة"
        )
    ]

    for text in examples:
        entities = extractor.extract(
            text
        )

        print("\n" + "=" * 70)
        print("Text:", text)

        print(
            json.dumps(
                entities,
                ensure_ascii=False,
                indent=4
            )
        )


if __name__ == "__main__":
    main()