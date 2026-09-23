# MoodleGuide API Benchmarks

## Environment

- Endpoint: `http://127.0.0.1:8000/v1/ask`
- Concurrent requests: 16
- Total requests: 50
- Successful requests: 50
- Failed requests: 0

## Results

| Metric | Result |
|---|---:|
| Success rate | 100.00% |
| Throughput | 29.20 requests/second |
| Minimum latency | 166.22 ms |
| Mean latency | 514.66 ms |
| p50 latency | 527.16 ms |
| p95 latency | 568.69 ms |
| p99 latency | 573.06 ms |
| Maximum latency | 575.47 ms |

## Notes

The measurement covers the complete `/v1/ask` pipeline:

1. Topic classification
2. Sentiment analysis
3. Entity extraction
4. Semantic search
5. Answer selection and routing

The results represent this machine and should not be copied to another environment.
