import re

from .preprocessing import mask_personal_data


class MoodleEntityExtractor:

    def __init__(self):
        self.file_pattern = re.compile(
            r"\b(pdf|docx?|xlsx?|pptx?|zip|rar|"
            r"png|jpe?g|mp4|csv)\b",
            re.IGNORECASE
        )

        self.date_pattern = re.compile(
            r"\b("
            r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
            r"|"
            r"\d{4}[/-]\d{1,2}[/-]\d{1,2}"
            r")\b"
        )

        self.error_code_pattern = re.compile(
            r"\b("
            r"error[\s_-]*\d+"
            r"|"
            r"خطأ[\s_-]*\d+"
            r"|"
            r"[45]\d{2}"
            r")\b",
            re.IGNORECASE
        )

        self.course_patterns = [
            re.compile(
                r"(?:مقرر|مادة)\s+"
                r"([\u0600-\u06FF\s]{3,40})"
            ),
            re.compile(
                r"(?:course|subject)\s+"
                r"([A-Za-z0-9\s]{3,40})",
                re.IGNORECASE
            )
        ]

        self.assignment_patterns = [
            re.compile(
                r"(?:الواجب|التكليف)\s*"
                r"([\u0600-\u06FF\d]+)?"
            ),
            re.compile(
                r"(?:assignment|homework)\s*"
                r"([A-Za-z0-9]+)?",
                re.IGNORECASE
            )
        ]

        self.quiz_patterns = [
            re.compile(
                r"(?:الاختبار|الكويز)\s*"
                r"([\u0600-\u06FF\d]+)?"
            ),
            re.compile(
                r"(?:quiz|exam|test)\s*"
                r"([A-Za-z0-9]+)?",
                re.IGNORECASE
            )
        ]

        self.feature_keywords = {
            "assignment": [
                "واجب",
                "الواجب",
                "تكليف",
                "assignment",
                "homework",
                "submission"
            ],
            "quiz": [
                "اختبار",
                "الاختبار",
                "كويز",
                "quiz",
                "exam",
                "test"
            ],
            "grades": [
                "درجة",
                "درجات",
                "الدرجات",
                "نتيجة",
                "grade",
                "grades",
                "mark",
                "marks"
            ],
            "attendance": [
                "حضور",
                "غياب",
                "الحضور",
                "الغياب",
                "attendance",
                "absence"
            ],
            "course": [
                "مقرر",
                "المقرر",
                "مادة",
                "course",
                "subject"
            ],
            "notification": [
                "إشعار",
                "اشعار",
                "تنبيه",
                "رسالة",
                "notification",
                "announcement"
            ],
            "virtual_class": [
                "فصل افتراضي",
                "محاضرة مباشرة",
                "محاضرة افتراضية",
                "virtual class",
                "online session",
                "live lecture"
            ],
            "login": [
                "تسجيل الدخول",
                "كلمة المرور",
                "الحساب",
                "login",
                "password",
                "account"
            ]
        }

    @staticmethod
    def add_entity(
        entities,
        entity_type,
        value
    ):
        if value is None:
            return

        value = str(value).strip(
            " ،,.!?؟:;"
        )

        if not value:
            return

        entity = {
            "type": entity_type,
            "value": value
        }

        if entity not in entities:
            entities.append(entity)

    def extract(
        self,
        text
    ):
        original_text = str(text).strip()

        if not original_text:
            return []

        safe_text = mask_personal_data(
            original_text
        )

        entities = []

        if "<PHONE>" in safe_text:
            self.add_entity(
                entities,
                "PERSONAL_DATA",
                "<PHONE>"
            )

        if "<EMAIL>" in safe_text:
            self.add_entity(
                entities,
                "PERSONAL_DATA",
                "<EMAIL>"
            )

        if "<NATIONAL_ID>" in safe_text:
            self.add_entity(
                entities,
                "PERSONAL_DATA",
                "<NATIONAL_ID>"
            )

        if "<STUDENT_ID>" in safe_text:
            self.add_entity(
                entities,
                "PERSONAL_DATA",
                "<STUDENT_ID>"
            )

        for match in self.file_pattern.finditer(
            safe_text
        ):
            self.add_entity(
                entities,
                "FILE_TYPE",
                match.group(1).lower()
            )

        for match in self.date_pattern.finditer(
            safe_text
        ):
            self.add_entity(
                entities,
                "DATE",
                match.group(1)
            )

        for match in (
            self.error_code_pattern.finditer(
                safe_text
            )
        ):
            self.add_entity(
                entities,
                "ERROR_CODE",
                match.group(1)
            )

        for pattern in self.course_patterns:
            match = pattern.search(
                safe_text
            )

            if match:
                self.add_entity(
                    entities,
                    "COURSE",
                    match.group(1)
                )
                break

        for pattern in self.assignment_patterns:
            match = pattern.search(
                safe_text
            )

            if match:
                value = match.group(0)

                self.add_entity(
                    entities,
                    "ASSIGNMENT",
                    value
                )
                break

        for pattern in self.quiz_patterns:
            match = pattern.search(
                safe_text
            )

            if match:
                value = match.group(0)

                self.add_entity(
                    entities,
                    "QUIZ",
                    value
                )
                break

        text_lower = safe_text.lower()

        for feature, keywords in (
            self.feature_keywords.items()
        ):
            if any(
                keyword.lower() in text_lower
                for keyword in keywords
            ):
                self.add_entity(
                    entities,
                    "MOODLE_FEATURE",
                    feature
                )

        return entities