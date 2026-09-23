import re
import unicodedata


PREPROCESSING_VERSION = "1.0.0"

PHONE_PATTERN = re.compile(r"(?:\+?966|0)5\d{8}")
NATIONAL_ID_PATTERN = re.compile(r"\b[12]\d{9}\b")
STUDENT_ID_PATTERN = re.compile(r"\b20\d{7,9}\b")
EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

ARABIC_DIACRITICS_PATTERN = re.compile(
    r"[\u0617-\u061A\u064B-\u0652]"
)

EXTRA_SPACES_PATTERN = re.compile(r"\s+")


def mask_personal_data(text: str) -> str:
    """Replace personal information with safe placeholders."""

    text = EMAIL_PATTERN.sub("<EMAIL>", text)
    text = PHONE_PATTERN.sub("<PHONE>", text)
    text = NATIONAL_ID_PATTERN.sub("<NATIONAL_ID>", text)
    text = STUDENT_ID_PATTERN.sub("<STUDENT_ID>", text)

    return text


def normalize_arabic(text: str) -> str:
    """Apply light Arabic normalization without changing meaning."""

    text = text.replace("ـ", "")
    text = ARABIC_DIACRITICS_PATTERN.sub("", text)

    text = re.sub("[إأآٱ]", "ا", text)
    text = text.replace("ى", "ي")

    return text


def normalize_text(text: str, language: str) -> str:
    """Normalize Arabic or English text."""

    text = unicodedata.normalize("NFC", str(text))

    if language == "ar":
        text = normalize_arabic(text)

    text = EXTRA_SPACES_PATTERN.sub(" ", text)

    return text.strip()


def preprocess_text(text: str, language: str) -> str:
    """Main preprocessing function used during training and serving."""

    text = mask_personal_data(text)
    text = normalize_text(text, language)

    return text