from src.moodleguide.semantic_search import (
    MoodleSemanticSearch
)


def main():
    print("Loading Moodle semantic search...")

    search_engine = MoodleSemanticSearch()

    queries = [
        {
            "text": "مادتي غير موجودة في الصفحة",
            "role": "student"
        },
        {
            "text": "كيف أضع امتحانا للطلبة؟",
            "role": "instructor"
        },
        {
            "text": "لا استطيع رفع ملف التكليف",
            "role": "student"
        },
        {
            "text": "كيف انشر درجات الطلاب؟",
            "role": "instructor"
        },
        {
            "text": "I cannot join the online lecture",
            "role": "student"
        }
    ]

    for query in queries:
        print("\n" + "=" * 60)
        print("Question:", query["text"])
        print("User role:", query["role"])

        results = search_engine.search(
            query=query["text"],
            user_role=query["role"],
            top_k=3
        )

        if not results:
            print("No results were found")
            continue

        for position, result in enumerate(
            results,
            start=1
        ):
            print(f"\nResult {position}")
            print("Score:", result["score"])
            print("Topic:", result["topic"])
            print(
                "Similar question:",
                result["question"]
            )
            print("Answer:", result["answer"])
            print(
                "Route to:",
                result["route_to"]
            )


if __name__ == "__main__":
    main()