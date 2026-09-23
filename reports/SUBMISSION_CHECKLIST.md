# MoodleGuide Submission Checklist

## 1. Source Code

- [ ] `src/moodleguide/api.py`
- [ ] `src/moodleguide/assistant.py`
- [ ] `src/moodleguide/preprocessing.py`
- [ ] `src/moodleguide/semantic_search.py`
- [ ] `src/moodleguide/embedding_model.py`
- [ ] `src/moodleguide/sentiment.py`
- [ ] `src/moodleguide/entity_extraction.py`
- [ ] `src/__init__.py`
- [ ] `src/moodleguide/__init__.py`

## 2. Dataset

- [ ] Raw dataset is available.
- [ ] Processed dataset is available.
- [ ] Training split is available.
- [ ] Validation split is available.
- [ ] Test split is available.
- [ ] Frozen test set is available.
- [ ] Frozen test manifest is available.
- [ ] No real personal data appears in the dataset.

## 3. Models

- [ ] TF-IDF baseline model is saved.
- [ ] Transformer topic classifier is saved.
- [ ] Tokenizer is saved with the Transformer model.
- [ ] FAISS search index is saved.
- [ ] Search metadata is saved.
- [ ] Search manifest is saved.
- [ ] Model files load without internet access.

## 4. Evaluation

- [ ] Baseline classification evaluation completed.
- [ ] Transformer evaluation completed.
- [ ] Model comparison completed.
- [ ] Semantic-search evaluation completed.
- [ ] Entity-extraction evaluation completed.
- [ ] API performance benchmark completed.
- [ ] Error files were reviewed.
- [ ] All reported results came from local runs.

## 5. Required Reports

- [ ] `reports/EVALUATION_REPORT.md`
- [ ] `reports/DECISIONS.md`
- [ ] `reports/BENCHMARKS.md`
- [ ] `reports/DEMO_SCRIPT.md`
- [ ] `README.md`
- [ ] `requirements.txt`

## 6. API Test

- [ ] `GET /health` returns `healthy`.
- [ ] `GET /topics` works.
- [ ] `POST /v1/ask` works in Arabic.
- [ ] `POST /v1/ask` works in English.
- [ ] Student questions return student guidance.
- [ ] Instructor questions return instructor guidance.
- [ ] Personal data is masked.
- [ ] Incorrect input returns a validation error.

## 7. Demo Questions

- [ ] Arabic student assignment example tested.
- [ ] Arabic instructor quiz example tested.
- [ ] English missing-course example tested.
- [ ] Personal-data masking example tested.
- [ ] Demonstration completed within five minutes.

## 8. Project Limitations

- [ ] Small dataset limitation documented.
- [ ] Template-generated data documented.
- [ ] Rule-based entity extraction documented.
- [ ] Sentiment-model limitation documented.
- [ ] CPU performance limitation documented.
- [ ] Future improvements documented.

## 9. Final Project Check

Run:

```powershell
python doctor.py