# MoodleGuide Technical Decisions

## 1. Project Purpose

MoodleGuide is a bilingual intelligent academic assistant for Moodle LMS.

The system helps students and instructors obtain guidance about Moodle features, retrieve relevant solutions, and route unresolved issues to the correct support department.

## 2. Supported Languages

The system supports:

- Arabic
- English

Arabic and English were selected because Moodle users may submit academic and technical questions in either language.

All programming identifiers and classification labels are written in English for technical consistency.

## 3. Supported Users

MoodleGuide supports two user roles:

- Student
- Instructor

The user role is included with every request.

Semantic-search results are filtered according to the selected role because students and instructors may require different answers to similar questions.

## 4. Topic Taxonomy

The system classifies questions into ten topics:

1. `login_access`
2. `course_enrollment`
3. `assignment`
4. `quiz_exam`
5. `grades`
6. `course_content`
7. `attendance`
8. `notifications`
9. `virtual_class`
10. `technical_problem`

These topics represent common Moodle support and academic-guidance requests.

## 5. Preprocessing

The project uses one versioned preprocessing module during training and API inference.

The preprocessing module performs:

- Unicode normalization
- Light Arabic normalization
- Removal of Arabic tatweel
- Whitespace normalization
- Personal-data masking

The system masks:

- Phone numbers
- National identification numbers
- Student identification numbers
- Email addresses

The project keeps words and expressions that may provide sentiment information.

The preprocessing version is stored with the processed dataset to reduce differences between training and deployment.

## 6. Baseline Model

TF-IDF with Logistic Regression was selected as the baseline topic-classification model.

Character n-grams were used because they can represent:

- Arabic word variations
- English words
- Spelling differences
- Short technical terms

The baseline provides a simple reference for evaluating the Transformer classifier.

## 7. Transformer Classifier

Multilingual DistilBERT was selected for topic classification.

The model supports Arabic and English and requires fewer computing resources than larger multilingual Transformer models.

The classifier predicts one of the ten Moodle topics and returns a confidence score.

The model was fine-tuned using the MoodleGuide training dataset.

## 8. Hybrid Topic Decision

The initial Transformer classifier sometimes produces low-confidence results because the training dataset is limited.

MoodleGuide uses the semantic-search topic when:

```text
Classifier confidence < 0.45
and
Semantic-search score >= 0.55

## 9. Semantic Search

MoodleGuide uses multilingual text embeddings to represent Moodle questions and answers as numerical vectors.

The semantic-search component uses:

- Multilingual MiniLM embeddings
- L2-normalized vectors
- FAISS `IndexFlatIP`
- Role-based result filtering

When vectors are normalized, inner-product similarity represents cosine similarity.

The FAISS index is stored with a manifest containing:

- Embedding model name
- Index type
- Vector dimension
- Document count
- Normalization setting

This allows the system to verify which model and settings produced the search index.

## 10. Role-Aware Retrieval

Students and instructors may ask similar questions but require different instructions.

For example, a student asking about an assignment needs submission instructions, while an instructor needs assignment-creation instructions.

MoodleGuide filters retrieved answers using the supplied user role:

- `student`
- `instructor`

This feature represents the selected project extension.

## 11. Sentiment Analysis

The project uses a pretrained multilingual sentiment model to classify questions as:

- `positive`
- `neutral`
- `negative`

The general sentiment model may not correctly understand common Moodle support expressions.

The system therefore applies domain rules for explicit phrases such as:

- لا أستطيع
- لا يعمل
- مشكلة
- cannot
- error
- not working

The API returns `sentiment_source` to show whether the final result came from:

- `model`
- `domain_rule`

## 12. Support Priority

MoodleGuide assigns support priority based on the final sentiment and topic.

High priority applies to negative requests related to:

- Quizzes and examinations
- Login access
- Technical problems

Other negative requests receive medium priority.

Neutral and positive questions receive normal priority.

This priority is intended to support ticket triage and does not replace institutional escalation policies.

## 13. Entity Extraction

The current prototype uses hybrid rule-based entity extraction.

It extracts:

- Moodle features
- Course names
- Assignments
- Quizzes
- File types
- Dates
- Error codes
- Masked personal data

Rule-based extraction was selected because the project does not yet have a sufficiently large labelled Moodle NER dataset.

The system must not describe this component as a fine-tuned Transformer NER model.

A future version can train a multilingual token-classification model using manually annotated Moodle questions.

## 14. API Design

MoodleGuide uses FastAPI to expose the system through HTTP.

The API provides:

- `GET /`
- `GET /health`
- `GET /topics`
- `POST /v1/ask`

The models load once when the application starts and remain available for subsequent requests.

Each `/v1/ask` request contains:

- Question text
- Language
- User role

The response contains:

- Predicted topic
- Topic source
- Classification confidence
- Sentiment
- Sentiment source
- Extracted entities
- Support priority
- Recommended answer
- Routing destination
- Similar questions

## 15. Evaluation

The project evaluates each component separately.

Topic classification uses:

- Accuracy
- Macro F1
- Classification report
- Confusion matrix

Semantic search uses:

- Recall@1
- Recall@3
- Recall@5
- Recall@10
- MRR@10

Entity extraction uses:

- Precision
- Recall
- F1
- Exact-match accuracy

API performance uses:

- Throughput
- Mean latency
- p50 latency
- p95 latency
- p99 latency

## 16. Frozen Test Data

The project uses a frozen test set containing questions that differ from the template-generated training examples.

The frozen test set must not be used for:

- Training
- Hyperparameter selection
- Expanding training templates
- Manual adjustment of individual predictions

The test-set hash is stored in a manifest to detect unintended changes.

## 17. Privacy

MoodleGuide masks personal information before processing.

The system must not store or display actual:

- Phone numbers
- National identification numbers
- Student identification numbers
- Email addresses

Production deployment would also require access control, secure logging, retention policies and institutional approval.

## 18. Performance

The API benchmark measures the complete `/v1/ask` pipeline on the local test machine.

The complete pipeline includes:

1. Topic classification
2. Sentiment analysis
3. Entity extraction
4. Semantic retrieval
5. Answer selection
6. Support routing

Benchmark results depend on the machine, model cache, Python environment and available GPU or CPU.

Only locally measured results should appear in `BENCHMARKS.md`.

## 19. Limitations

The prototype currently has the following limitations:

- The training dataset is small.
- Part of the training data is template-generated.
- The knowledge base contains a limited number of Moodle questions.
- The sentiment model was not fine-tuned on Moodle support data.
- Entity extraction currently relies on rules.
- CPU inference may have high latency.
- The evaluation datasets are suitable for a prototype, not production certification.

## 20. Future Improvements

Future work should include:

- Collecting independently written Moodle questions.
- Expanding the approved Moodle knowledge base.
- Training a Moodle-specific NER model.
- Fine-tuning sentiment analysis on academic-support data.
- Exporting classification models to ONNX.
- Applying dynamic INT8 quantization.
- Adding authentication and secure logging.
- Integrating the assistant with Moodle web services.
- Conducting usability testing with students and instructors.