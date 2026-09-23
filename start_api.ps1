Write-Host "========================================"
Write-Host "Starting MoodleGuide"
Write-Host "Python version:"
python --version
Write-Host "========================================"

Write-Host "Running project checks..."

python doctor.py

Write-Host "Starting MoodleGuide API..."

python -m uvicorn src.moodleguide.api:app `
    --host 127.0.0.1 `
    --port 8000