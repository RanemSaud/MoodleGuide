# MoodleGuide Five-Minute Demo

## Project Title

**MoodleGuide: A Bilingual Intelligent Academic Assistant for Moodle LMS**

## 0:00–0:40 — Introduction

MoodleGuide is a bilingual intelligent assistant designed to help students and instructors use Moodle.

The system accepts Arabic and English questions and performs topic classification, sentiment analysis, entity extraction, semantic search and support routing.

The selected project extension is role-aware guidance, which provides different answers for students and instructors.

## 0:40–1:10 — System Architecture

The user submits:

- A question
- A language
- A user role

The system then:

1. Masks personal data.
2. Classifies the Moodle topic.
3. Analyzes sentiment.
4. Extracts Moodle entities.
5. Searches the knowledge base.
6. Selects a role-appropriate answer.
7. Assigns priority and routing.

## 1:10–2:15 — Arabic Student Demonstration

Open:

```text
http://127.0.0.1:8000/docs
```

Select:

```text
POST /v1/ask
```

Use:

```json
{
  "text": "لا أستطيع رفع ملف PDF في الواجب الثالث لمقرر معالجة اللغة الطبيعية",
  "language": "ar",
  "user_role": "student"
}
```

Explain the response:

- The topic should relate to assignments.
- The sentiment should be negative.
- The system extracts `PDF`.
- The system extracts the assignment.
- The system extracts the course name.
- The answer provides submission guidance.
- The issue is routed to the appropriate support destination.

## 2:15–3:00 — Instructor Demonstration

Use:

```json
{
  "text": "كيف أضيف اختبارا جديدا للطلاب؟",
  "language": "ar",
  "user_role": "instructor"
}
```

Explain:

- The user role is `instructor`.
- The topic is `quiz_exam`.
- The answer explains how to create a quiz.
- The system does not provide student instructions.
- This demonstrates role-aware guidance.

## 3:00–3:40 — English Demonstration

Use:

```json
{
  "text": "My course is missing from the Moodle dashboard",
  "language": "en",
  "user_role": "student"
}
```

Explain:

- MoodleGuide supports English and Arabic.
- The expected topic is `course_enrollment`.
- The system retrieves a similar question.
- The issue is routed to the registration department.

## 3:40–4:10 — Privacy Demonstration

Use:

```json
{
  "text": "رقم جوالي 0501234567 ولا أستطيع الدخول إلى حسابي",
  "language": "ar",
  "user_role": "student"
}
```

Explain:

- The phone number is detected as personal data.
- The preprocessing component replaces it with `<PHONE>`.
- The real phone number must not appear in model logs or training data.

## 4:10–4:40 — Evaluation Results

Open:

```text
reports/EVALUATION_REPORT.md
```

Present:

- Baseline Macro F1
- Transformer Macro F1
- Semantic-search Recall@10
- Semantic-search MRR@10
- Entity-extraction F1
- API p99 latency

Only present values produced by local evaluation scripts.

## 4:40–5:00 — Conclusion

MoodleGuide demonstrates an end-to-end bilingual NLP application for Moodle.

The prototype combines classification, retrieval, sentiment, entity extraction and role-aware routing.

The main limitation is the size of the current dataset.

The next step is to collect more independently written and anonymized Moodle questions and optimize the models for production inference.

# Expected Challenge Question

## Why should we trust the retrieval result?

The search component was evaluated on a frozen set of new questions.

The project reports Recall@10 and MRR@10 and stores individual retrieval errors for review.

The test set was excluded from training and index development.

# Backup Questions

## Why use Multilingual DistilBERT?

It supports Arabic and English while requiring fewer computational resources than larger multilingual Transformer models.

## Why use TF-IDF?

TF-IDF provides a simple and interpretable baseline for measuring whether the Transformer improves topic classification.

## Why use FAISS?

FAISS provides efficient vector similarity search and allows the system to retrieve semantically related Moodle questions.

## Why combine classification and retrieval?

The classifier may produce an uncertain result when training data is limited.

The search result provides additional evidence from the Moodle knowledge base.

## Is the entity extractor a Transformer NER model?

No. The current prototype uses hybrid rule-based entity extraction.

A future version can train a token-classification model after creating a larger manually annotated dataset.

## What is the main project extension?

The extension is role-aware academic guidance and support routing for students and instructors.