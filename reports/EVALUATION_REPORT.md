# MoodleGuide Evaluation Report

## Project Overview

MoodleGuide is a bilingual intelligent academic assistant for Moodle LMS.

The system supports Arabic and English questions from students and instructors.

## Topic Classification Results

| Model | Accuracy | Macro F1 |
|---|---:|---:|
| TF-IDF and Logistic Regression | 0.3000 | 0.2447 |
| Multilingual DistilBERT | 0.2000 | 0.1952 |

## Semantic Search Results

| Metric | Result |
|---|---:|
| Recall@1 | 0.4333 |
| Recall@3 | 0.6333 |
| Recall@10 | 0.9000 |
| MRR@10 | 0.5782 |

## API Performance

| Metric | Result |
|---|---:|
| Successful requests | {format_number(successful_requests)} |
| Throughput, requests/second | {format_number(throughput)} |
| Mean latency, ms | {format_number(mean_latency)} |
| p50 latency, ms | {format_number(p50_latency)} |
| p95 latency, ms | {format_number(p95_latency)} |
| p99 latency, ms | {format_number(p99_latency)} |

The benchmark covers the complete `/v1/ask` pipeline on the test machine.

## Notes

The TF-IDF model is the baseline model.

Multilingual DistilBERT is the Transformer model.

The frozen test dataset was not used during training.
