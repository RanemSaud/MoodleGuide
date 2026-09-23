from pathlib import Path
import importlib.util
import platform
import sys


required_packages = {
    "pandas": "pandas",
    "numpy": "numpy",
    "scikit-learn": "sklearn",
    "joblib": "joblib",
    "PyTorch": "torch",
    "Transformers": "transformers",
    "Datasets": "datasets",
    "Accelerate": "accelerate",
    "FAISS": "faiss",
    "FastAPI": "fastapi",
    "Uvicorn": "uvicorn",
    "Pydantic": "pydantic",
    "Requests": "requests"
}


required_files = [
    "data/raw/moodle_inquiries.csv",
    "data/processed/splits/train.csv",
    "data/processed/splits/validation.csv",
    "data/processed/splits/test.csv",
    "data/test/frozen_test.csv",

    "models/baseline/topic_classifier.joblib",

    "models/transformer/"
    "topic_classifier/config.json",

    "models/semantic_search/"
    "moodle_knowledge.index",

    "models/semantic_search/"
    "metadata.csv",

    "models/semantic_search/"
    "manifest.json",

    "src/moodleguide/"
    "preprocessing.py",

    "src/moodleguide/"
    "embedding_model.py",

    "src/moodleguide/"
    "semantic_search.py",

    "src/moodleguide/"
    "sentiment.py",

    "src/moodleguide/"
    "entity_extraction.py",

    "src/moodleguide/"
    "assistant.py",

    "src/moodleguide/"
    "api.py",

    "reports/"
    "EVALUATION_REPORT.md",

    "reports/"
    "DECISIONS.md",

    "README.md",
    "requirements.txt"
]


def print_result(
    status,
    message
):
    symbol = (
        "[PASS]"
        if status
        else "[FAIL]"
    )

    print(
        f"{symbol} {message}"
    )


def check_python():
    print("\nPython Environment")

    version = sys.version_info

    print(
        "Python version:",
        platform.python_version()
    )

    print(
        "Executable:",
        sys.executable
    )

    supported = (
    version.major == 3
    and version.minor >= 12
    )

    print_result(
        supported,
        (
            "Python version is supported"
            if supported
            else
            "Python 3.14 is recommended"
        )
    )

    return supported


def check_packages():
    print("\nPython Packages")

    passed = True

    for package_name, module_name in (
        required_packages.items()
    ):
        installed = (
            importlib.util.find_spec(
                module_name
            )
            is not None
        )

        print_result(
            installed,
            package_name
        )

        if not installed:
            passed = False

    return passed


def check_files():
    print("\nProject Files")

    passed = True

    for filename in required_files:
        exists = Path(filename).exists()

        print_result(
            exists,
            filename
        )

        if not exists:
            passed = False

    return passed


def check_model_files():
    print("\nModel Details")

    transformer_folder = Path(
        "models/transformer/"
        "topic_classifier"
    )

    transformer_model_exists = any(
        transformer_folder.glob(
            "*.safetensors"
        )
    ) or any(
        transformer_folder.glob(
            "pytorch_model*.bin"
        )
    )

    print_result(
        transformer_model_exists,
        "Transformer model weights"
    )

    return transformer_model_exists


def main():
    print("=" * 60)
    print("MoodleGuide Project Doctor")
    print("=" * 60)

    python_ok = check_python()
    packages_ok = check_packages()
    files_ok = check_files()
    models_ok = check_model_files()

    print("\n" + "=" * 60)
    print("Final Result")
    print("=" * 60)

    if (
        packages_ok
        and files_ok
        and models_ok
    ):
        print(
            "[READY] MoodleGuide is ready "
            "for testing and demonstration."
        )

        if not python_ok:
            print(
                "[WARNING] The project is ready, "
                "but Python 3.14 is recommended."
            )

    else:
        print(
            "[NOT READY] Some required "
            "items are missing."
        )

        print(
            "Review the [FAIL] entries above."
        )


if __name__ == "__main__":
    main()
