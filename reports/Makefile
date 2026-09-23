.PHONY: doctor serve test reports benchmark

doctor:
	python doctor.py

serve:
	python -m uvicorn src.moodleguide.api:app --host 127.0.0.1 --port 8000

test:
	python test_assistant.py

reports:
	python generate_reports.py

benchmark:
	python benchmark_api.py