from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from pathlib import Path
import json
import statistics
import time

import numpy as np
import requests


API_URL = (
    "http://127.0.0.1:8000/v1/ask"
)

CONCURRENT_REQUESTS = 16
TOTAL_REQUESTS = 50
WARMUP_REQUESTS = 3
TIMEOUT_SECONDS = 120

REPORT_FOLDER = Path("reports")
REPORT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


payloads = [
    {
        "text": (
            "لا أستطيع رفع ملف PDF "
            "في الواجب الثالث"
        ),
        "language": "ar",
        "user_role": "student"
    },
    {
        "text": (
            "كيف أضيف اختبارا "
            "جديدا للطلاب؟"
        ),
        "language": "ar",
        "user_role": "instructor"
    },
    {
        "text": (
            "The course is missing "
            "from my dashboard"
        ),
        "language": "en",
        "user_role": "student"
    },
    {
        "text": (
            "Students cannot view "
            "their final grades"
        ),
        "language": "en",
        "user_role": "instructor"
    },
    {
        "text": (
            "لا أستطيع الدخول إلى "
            "الاختبار وأنا منزعج"
        ),
        "language": "ar",
        "user_role": "student"
    }
]


def send_request(request_number):
    payload = payloads[
        request_number % len(payloads)
    ]

    start_time = time.perf_counter()

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=TIMEOUT_SECONDS
        )

        elapsed_ms = (
            time.perf_counter()
            - start_time
        ) * 1000

        return {
            "request_number": request_number,
            "success": (
                response.status_code == 200
            ),
            "status_code": (
                response.status_code
            ),
            "latency_ms": round(
                elapsed_ms,
                4
            ),
            "error": None
        }

    except Exception as error:
        elapsed_ms = (
            time.perf_counter()
            - start_time
        ) * 1000

        return {
            "request_number": request_number,
            "success": False,
            "status_code": None,
            "latency_ms": round(
                elapsed_ms,
                4
            ),
            "error": str(error)
        }


def main():
    print("Checking API health...")

    try:
        health_response = requests.get(
            "http://127.0.0.1:8000/health",
            timeout=30
        )

        health_response.raise_for_status()

    except Exception as error:
        raise RuntimeError(
            "The API is not running. "
            "Start Uvicorn before running "
            "the benchmark."
        ) from error

    print("Running warm-up requests...")

    for index in range(WARMUP_REQUESTS):
        result = send_request(index)

        print(
            f"Warm-up {index + 1}: "
            f"{result['latency_ms']:.2f} ms"
        )

    print("\nStarting benchmark...")
    print(
        "Concurrent requests:",
        CONCURRENT_REQUESTS
    )
    print(
        "Total requests:",
        TOTAL_REQUESTS
    )

    benchmark_start = (
        time.perf_counter()
    )

    results = []

    with ThreadPoolExecutor(
        max_workers=CONCURRENT_REQUESTS
    ) as executor:
        futures = [
            executor.submit(
                send_request,
                request_number
            )
            for request_number
            in range(TOTAL_REQUESTS)
        ]

        for future in as_completed(
            futures
        ):
            result = future.result()
            results.append(result)

            print(
                f"Request "
                f"{result['request_number'] + 1}: "
                f"{result['latency_ms']:.2f} ms "
                f"status={result['status_code']}"
            )

    total_time_seconds = (
        time.perf_counter()
        - benchmark_start
    )

    successful_results = [
        result
        for result in results
        if result["success"]
    ]

    failed_results = [
        result
        for result in results
        if not result["success"]
    ]

    if not successful_results:
        raise RuntimeError(
            "All benchmark requests failed"
        )

    latencies = np.array(
        [
            result["latency_ms"]
            for result in successful_results
        ],
        dtype=float
    )

    metrics = {
        "endpoint": API_URL,
        "concurrency": CONCURRENT_REQUESTS,
        "total_requests": TOTAL_REQUESTS,
        "successful_requests": len(
            successful_results
        ),
        "failed_requests": len(
            failed_results
        ),
        "success_rate": round(
            len(successful_results)
            / TOTAL_REQUESTS,
            4
        ),
        "total_time_seconds": round(
            total_time_seconds,
            4
        ),
        "throughput_requests_per_second": round(
            len(successful_results)
            / total_time_seconds,
            4
        ),
        "latency_ms": {
            "minimum": round(
                float(np.min(latencies)),
                4
            ),
            "mean": round(
                float(np.mean(latencies)),
                4
            ),
            "median": round(
                float(
                    statistics.median(latencies)
                ),
                4
            ),
            "p50": round(
                float(
                    np.percentile(
                        latencies,
                        50
                    )
                ),
                4
            ),
            "p95": round(
                float(
                    np.percentile(
                        latencies,
                        95
                    )
                ),
                4
            ),
            "p99": round(
                float(
                    np.percentile(
                        latencies,
                        99
                    )
                ),
                4
            ),
            "maximum": round(
                float(np.max(latencies)),
                4
            )
        }
    }

    json_file = (
        REPORT_FOLDER
        / "api_benchmark.json"
    )

    details_file = (
        REPORT_FOLDER
        / "api_benchmark_details.json"
    )

    markdown_file = (
        REPORT_FOLDER
        / "BENCHMARKS.md"
    )

    with open(
        json_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            metrics,
            file,
            ensure_ascii=False,
            indent=4
        )

    with open(
        details_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            sorted(
                results,
                key=lambda item: (
                    item["request_number"]
                )
            ),
            file,
            ensure_ascii=False,
            indent=4
        )

    markdown_content = f"""# MoodleGuide API Benchmarks

## Environment

- Endpoint: `{API_URL}`
- Concurrent requests: {CONCURRENT_REQUESTS}
- Total requests: {TOTAL_REQUESTS}
- Successful requests: {len(successful_results)}
- Failed requests: {len(failed_results)}

## Results

| Metric | Result |
|---|---:|
| Success rate | {metrics["success_rate"]:.2%} |
| Throughput | {metrics["throughput_requests_per_second"]:.2f} requests/second |
| Minimum latency | {metrics["latency_ms"]["minimum"]:.2f} ms |
| Mean latency | {metrics["latency_ms"]["mean"]:.2f} ms |
| p50 latency | {metrics["latency_ms"]["p50"]:.2f} ms |
| p95 latency | {metrics["latency_ms"]["p95"]:.2f} ms |
| p99 latency | {metrics["latency_ms"]["p99"]:.2f} ms |
| Maximum latency | {metrics["latency_ms"]["maximum"]:.2f} ms |

## Notes

The measurement covers the complete `/v1/ask` pipeline:

1. Topic classification
2. Sentiment analysis
3. Entity extraction
4. Semantic search
5. Answer selection and routing

The results represent this machine and should not be copied to another environment.
"""

    markdown_file.write_text(
        markdown_content,
        encoding="utf-8"
    )

    print("\nBenchmark completed")
    print(
        "Success rate:",
        f"{metrics['success_rate']:.2%}"
    )
    print(
        "Throughput:",
        metrics[
            "throughput_requests_per_second"
        ],
        "requests/second"
    )
    print(
        "p50:",
        metrics["latency_ms"]["p50"],
        "ms"
    )
    print(
        "p95:",
        metrics["latency_ms"]["p95"],
        "ms"
    )
    print(
        "p99:",
        metrics["latency_ms"]["p99"],
        "ms"
    )

    print("\nReports saved:")
    print(json_file)
    print(details_file)
    print(markdown_file)


if __name__ == "__main__":
    main()