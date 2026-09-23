import json
from pathlib import Path

import pandas as pd


reports_folder = Path("reports")

with open(
    reports_folder / "frozen_baseline_metrics.json",
    encoding="utf-8"
) as file:
    baseline = json.load(file)

with open(
    reports_folder / "frozen_transformer_metrics.json",
    encoding="utf-8"
) as file:
    transformer = json.load(file)


comparison = pd.DataFrame(
    [
        {
            "model": "TF-IDF + Logistic Regression",
            "accuracy": baseline["accuracy"],
            "macro_f1": baseline["macro_f1"]
        },
        {
            "model": "Multilingual DistilBERT",
            "accuracy": transformer["accuracy"],
            "macro_f1": transformer["macro_f1"]
        }
    ]
)

baseline_f1 = baseline["macro_f1"]
transformer_f1 = transformer["macro_f1"]

difference = transformer_f1 - baseline_f1

if baseline_f1 > 0:
    relative_improvement = (
        difference / baseline_f1
    ) * 100
else:
    relative_improvement = 0


print(comparison.to_string(index=False))

print("\nMacro-F1 difference:", round(difference, 4))
print(
    "Relative improvement:",
    f"{relative_improvement:.2f}%"
)


comparison.to_csv(
    reports_folder / "model_comparison.csv",
    index=False,
    encoding="utf-8-sig"
)