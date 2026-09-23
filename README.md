# MoodleGuide

## Bilingual Intelligent Academic Assistant for Moodle LMS

MoodleGuide is a bilingual intelligent academic assistant that helps students and instructors use the Moodle Learning Management System.

The system accepts questions in Arabic or English, identifies the question topic, analyzes sentiment, extracts Moodle-related entities, retrieves relevant guidance and routes unresolved issues to the appropriate support department.

## Project Features

MoodleGuide provides:

- Arabic and English support
- Student and instructor guidance
- Moodle topic classification
- Sentiment analysis
- Moodle entity extraction
- Semantic search using FAISS
- Role-aware answer retrieval
- Support priority assignment
- Automatic support routing
- FastAPI REST interface
- Model and retrieval evaluation
- HTTP performance benchmarking

## Supported Topics

The system classifies questions into ten categories:

| Topic | Description |
|---|---|
| `login_access` | Login, password and account access |
| `course_enrollment` | Course enrolment and missing courses |
| `assignment` | Assignment creation and submission |
| `quiz_exam` | Quizzes, examinations and attempts |
| `grades` | Grades, marks and result visibility |
| `course_content` | Files, lectures and course resources |
| `attendance` | Attendance and absence records |
| `notifications` | Notifications, messages and announcements |
| `virtual_class` | Virtual classrooms and online sessions |
| `technical_problem` | General Moodle technical problems |

## Supported Users

MoodleGuide supports:

- Students
- Instructors

The user role affects the retrieved answer.

For example:

- A student receives assignment-submission instructions.
- An instructor receives assignment-creation instructions.

## Project Architecture

The system follows this processing flow:

```text
User question
    |
    v
Input validation
    |
    v
Personal-data masking and preprocessing
    |
    +----------------------+
    |                      |
    v                      v
Topic classification   Sentiment analysis
    |                      |
    +----------+-----------+
               |
               v
        Entity extraction
               |
               v
        Semantic search
               |
               v
   Role-aware answer selection
               |
               v
     Priority and support routing
               |
               v
         FastAPI response
```

## Project Structure

```text
MoodleGuide/
├── data/
│   ├── raw/
│   │   └── moodle_inquiries.csv
│   ├── processed/
│   │   ├── moodle_inquiries_processed.csv
│   │   ├── moodle_inquiries_expanded.csv
│   │   └── splits/
│   │       ├── train.csv
│   │       ├── validation.csv
│   │       └── test.csv
│   └── test/
│       ├── frozen_test.csv
│       ├── frozen_test_manifest.txt
│       └── entity_test.json
│
├── models/
│   ├── baseline/
│   │   └── topic_classifier.joblib
│   ├── transformer/
│   │   └── topic_classifier/
│   └── semantic_search/
│       ├── moodle_knowledge.index
│       ├── metadata.csv
│       └── manifest.json
│
├── reports/
│   ├── EVALUATION_REPORT.md
│   ├── DECISIONS.md
│   ├── BENCHMARKS.md
│   ├── baseline_metrics.json
│   ├── frozen_baseline_metrics.json
│   ├── frozen_transformer_metrics.json
│   ├── semantic_search_metrics.json
│   ├── entity_metrics.json
│   └── api_benchmark.json
│
├── src/
│   ├── __init__.py
│   └── moodleguide/
│       ├── __init__.py
│       ├── api.py
│       ├── assistant.py
│       ├── embedding_model.py
│       ├── entity_extraction.py
│       ├── preprocessing.py
│       ├── semantic_search.py
│       └── sentiment.py
│
├── benchmark_api.py
├── build_search_index.py
├── compare_models.py
├── create_dataset.py
├── create_entity_test.py
├── create_frozen_test.py
├── evaluate_entity_extraction.py
├── evaluate_frozen_test.py
├── evaluate_semantic_search.py
├── evaluate_transformer.py
├── expand_dataset.py
├── generate_reports.py
├── process_dataset.py
├── split_dataset.py
├── test_assistant.py
├── test_baseline.py
├── test_entity_extraction.py
├── test_semantic_search.py
├── test_sentiment.py
├── test_transformer.py
├── train_baseline.py
├── train_transformer.py
├── requirements.txt
└── README.md
```

## System Requirements

Recommended environment:

- Windows 10 or Windows 11
- Visual Studio Code
- Python 3.14
- At least 8 GB RAM
- Internet access for initial model downloads
- Optional NVIDIA GPU for faster training and inference

Python 3.14 is recommended to reduce compatibility problems with machine-learning libraries.

## Installation

### 1. Open the Project

Open the `MoodleGuide` folder in Visual Studio Code.

### 2. Create a Virtual Environment

Open a new terminal:

```powershell
py -3.14 -m venv .venv
```

Activate it:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Confirm the Python version:

```powershell
python --version
```

Expected output:

```text
Python 3.14.x
```

### 3. Select the Python Interpreter

In Visual Studio Code:

```text
Ctrl + Shift + P
```

Select:

```text
Python: Select Interpreter
```

Choose:

```text
MoodleGuide\.venv\Scripts\python.exe
```

### 4. Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the Hugging Face Trainer reports a missing `accelerate` package:

```powershell
python -m pip install --upgrade "accelerate>=1.1.0" "transformers[torch]"
```

## Dependencies

The `requirements.txt` file should contain:

```text
pandas
numpy
scikit-learn
joblib
torch
transformers
datasets
accelerate
faiss-cpu
fastapi
uvicorn
pydantic
requests
sentence-transformers
seqeval
```

The current embedding implementation uses Hugging Face Transformers directly. The `sentence-transformers` package can remain installed for experiments and future development.

## Recommended Execution Order

### Stage 1: Create and Process the Dataset

```powershell
python create_dataset.py
python process_dataset.py
python expand_dataset.py
python split_dataset.py
```

Expected files:

```text
data/raw/moodle_inquiries.csv
data/processed/moodle_inquiries_processed.csv
data/processed/moodle_inquiries_expanded.csv
data/processed/splits/train.csv
data/processed/splits/validation.csv
data/processed/splits/test.csv
```

### Stage 2: Train the Baseline Model

```powershell
python train_baseline.py
```

Test it:

```powershell
python test_baseline.py
```

### Stage 3: Create the Frozen Test Set

```powershell
python create_frozen_test.py
```

Evaluate the baseline:

```powershell
python evaluate_frozen_test.py
```

The frozen test dataset must not be used for training.

### Stage 4: Train the Transformer Classifier

```powershell
python train_transformer.py
```

Test it:

```powershell
python test_transformer.py
```

Evaluate it:

```powershell
python evaluate_transformer.py
```

Compare the two classifiers:

```powershell
python compare_models.py
```

### Stage 5: Build Semantic Search

```powershell
python build_search_index.py
```

Test the search engine:

```powershell
python test_semantic_search.py
```

Evaluate retrieval:

```powershell
python evaluate_semantic_search.py
```

### Stage 6: Test Sentiment Analysis

```powershell
python test_sentiment.py
```

### Stage 7: Test Entity Extraction

```powershell
python test_entity_extraction.py
```

Create the entity test set:

```powershell
python create_entity_test.py
```

Evaluate entity extraction:

```powershell
python evaluate_entity_extraction.py
```

### Stage 8: Test the Complete Assistant

```powershell
python test_assistant.py
```

### Stage 9: Generate Reports

```powershell
python generate_reports.py
```

Generated reports:

```text
reports/EVALUATION_REPORT.md
reports/DECISIONS.md
reports/BENCHMARKS.md
```

## Running the API

Start the FastAPI server:

```powershell
python -m uvicorn src.moodleguide.api:app
```

Wait until the terminal displays:

```text
MoodleGuide assistant is ready
MoodleGuide API is ready
Uvicorn running on http://127.0.0.1:8000
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

Expected health response:

```json
{
  "status": "healthy",
  "assistant_ready": true
}
```

## API Usage

### Endpoint

```http
POST /v1/ask
```

### Arabic Student Example

```json
{
  "text": "لا أستطيع رفع ملف PDF في الواجب الثالث",
  "language": "ar",
  "user_role": "student"
}
```

### Arabic Instructor Example

```json
{
  "text": "كيف أضيف اختبارا جديدا للطلاب؟",
  "language": "ar",
  "user_role": "instructor"
}
```

### English Student Example

```json
{
  "text": "My course is missing from the dashboard",
  "language": "en",
  "user_role": "student"
}
```

### Example Response

```json
{
  "question": "لا أستطيع الدخول إلى الاختبار",
  "language": "ar",
  "user_role": "student",
  "predicted_topic": "quiz_exam",
  "topic_source": "semantic_search",
  "classification_confidence": 0.1891,
  "sentiment": "negative",
  "sentiment_confidence": 0.4321,
  "sentiment_source": "domain_rule",
  "sentiment_scores": {
    "positive": 0.2075,
    "neutral": 0.4321,
    "negative": 0.3604
  },
  "entities": [
    {
      "type": "QUIZ",
      "value": "الاختبار"
    },
    {
      "type": "MOODLE_FEATURE",
      "value": "quiz"
    }
  ],
  "support_priority": "high",
  "answer": "تحقق من وقت الاختبار ثم تواصل مباشرة مع مدرس المقرر.",
  "route_to": "Course Instructor",
  "search_score": 0.6804,
  "similar_questions": [
    {
      "question": "تم إغلاق الاختبار قبل إكمال المحاولة",
      "topic": "quiz_exam",
      "score": 0.6804
    }
  ]
}
```

The numerical values above are examples. Actual values depend on the locally trained models and machine environment.

## API Performance Benchmark

The API must be running before starting the benchmark.

### Terminal 1

```powershell
python -m uvicorn src.moodleguide.api:app
```

### Terminal 2

```powershell
python benchmark_api.py
```

The benchmark creates:

```text
reports/api_benchmark.json
reports/api_benchmark_details.json
reports/BENCHMARKS.md
```

After benchmarking, update the evaluation report:

```powershell
python generate_reports.py
```

## Evaluation Metrics

### Topic Classification

- Accuracy
- Macro F1
- Per-class precision
- Per-class recall
- Confusion matrix

### Semantic Search

- Recall@1
- Recall@3
- Recall@5
- Recall@10
- MRR@10

### Entity Extraction

- Precision
- Recall
- F1
- Exact-match accuracy

### API Performance

- Success rate
- Throughput
- Mean latency
- p50 latency
- p95 latency
- p99 latency

## Hybrid Decision Logic

MoodleGuide uses the semantic-search topic when:

```text
Classifier confidence < 0.45
and
Semantic-search score >= 0.55
```

Otherwise, it keeps the Transformer prediction.

The API reports the source through:

```text
topic_source
```

Possible values:

```text
classifier
semantic_search
```

## Support Priority

The system assigns priority as follows:

| Condition | Priority |
|---|---|
| Negative quiz, login or technical issue | High |
| Other negative question | Medium |
| Neutral or positive question | Normal |

## Support Routing

Example routing:

| Topic | Destination |
|---|---|
| Login or account problem | IT Support |
| Missing course | Registration Department |
| Assignment submission issue | Course Instructor or eLearning Support |
| Quiz or examination issue | Course Instructor |
| Grade issue | Course Instructor |
| Moodle configuration issue | eLearning Support |

## Privacy

MoodleGuide masks personal information before processing.

Protected values include:

- Phone numbers
- National identification numbers
- Student identification numbers
- Email addresses

Actual personal values must not appear in training data, logs or API responses.

## Reports

### Evaluation Report

```text
reports/EVALUATION_REPORT.md
```

Contains classification, retrieval, entity-extraction and performance results.

### Technical Decisions

```text
reports/DECISIONS.md
```

Explains the design choices, thresholds, models, privacy controls and limitations.

### Benchmarks

```text
reports/BENCHMARKS.md
```

Contains latency and throughput measurements collected from the local machine.

## Current Limitations

- The training dataset is small.
- Part of the training data is generated from templates.
- The knowledge base contains a limited number of Moodle questions.
- Sentiment analysis is not fine-tuned on Moodle support data.
- Entity extraction currently uses domain rules.
- CPU inference may be slow.
- The current evaluation represents a prototype.
- Production use requires approved Moodle documentation and security controls.

## Future Development

Future improvements may include:

- Collecting real, anonymized Moodle questions.
- Expanding the Arabic and English knowledge base.
- Training a Moodle-specific NER model.
- Fine-tuning sentiment analysis on academic-support data.
- Exporting the classifier to ONNX.
- Applying dynamic INT8 quantization.
- Adding authentication and secure audit logging.
- Integrating with Moodle web services.
- Adding a graphical web interface.
- Conducting usability tests with students and instructors.

## Project Extension

The selected extension is:

```text
Role-Aware Academic Guidance and Support Routing
```

This extension provides different answers for students and instructors and routes unresolved requests to the relevant department.

## Academic Integrity

All reported metrics must come from local project runs.

The frozen test dataset must not be used during training.

Copied benchmark results must not be included in the final report.

## Stopping the API

To stop Uvicorn, return to its terminal and press:

```text
Ctrl + C
```

## Project Status

The prototype currently includes:

- Bilingual preprocessing
- Baseline topic classification
- Transformer topic classification
- Sentiment analysis
- Entity extraction
- Semantic search
- Role-aware responses
- Priority and support routing
- FastAPI serving
- Evaluation scripts
- Benchmark scripts
- Technical reports