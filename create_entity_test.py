from pathlib import Path
import json


test_cases = [
    {
        "text": "أريد رفع ملف PDF في الواجب الثالث",
        "expected_entities": [
            {
                "type": "FILE_TYPE",
                "value": "pdf"
            },
            {
                "type": "ASSIGNMENT",
                "value": "الواجب الثالث"
            },
            {
                "type": "MOODLE_FEATURE",
                "value": "assignment"
            }
        ]
    },
    {
        "text": "يظهر خطأ 403 عند فتح الاختبار",
        "expected_entities": [
            {
                "type": "ERROR_CODE",
                "value": "403"
            },
            {
                "type": "QUIZ",
                "value": "الاختبار"
            },
            {
                "type": "MOODLE_FEATURE",
                "value": "quiz"
            }
        ]
    },
    {
        "text": "موعد تسليم التكليف هو 25/09/2026",
        "expected_entities": [
            {
                "type": "DATE",
                "value": "25/09/2026"
            },
            {
                "type": "ASSIGNMENT",
                "value": "التكليف"
            },
            {
                "type": "MOODLE_FEATURE",
                "value": "assignment"
            }
        ]
    },
    {
        "text": "لا تظهر درجات مقرر البرمجة",
        "expected_entities": [
            {
                "type": "COURSE",
                "value": "البرمجة"
            },
            {
                "type": "MOODLE_FEATURE",
                "value": "grades"
            },
            {
                "type": "MOODLE_FEATURE",
                "value": "course"
            }
        ]
    },
    {
        "text": "كيف أعيد تعيين كلمة المرور؟",
        "expected_entities": [
            {
                "type": "MOODLE_FEATURE",
                "value": "login"
            }
        ]
    },
    {
        "text": "رابط المحاضرة المباشرة لا يعمل",
        "expected_entities": [
            {
                "type": "MOODLE_FEATURE",
                "value": "virtual_class"
            }
        ]
    },
    {
        "text": "I cannot upload a DOCX assignment",
        "expected_entities": [
            {
                "type": "FILE_TYPE",
                "value": "docx"
            },
            {
                "type": "ASSIGNMENT",
                "value": "assignment"
            },
            {
                "type": "MOODLE_FEATURE",
                "value": "assignment"
            }
        ]
    },
    {
        "text": "Error 500 appears when opening Quiz 2",
        "expected_entities": [
            {
                "type": "ERROR_CODE",
                "value": "error 500"
            },
            {
                "type": "QUIZ",
                "value": "Quiz 2"
            },
            {
                "type": "MOODLE_FEATURE",
                "value": "quiz"
            }
        ]
    },
    {
        "text": "Upload the slides to the Python course",
        "expected_entities": [
            {
                "type": "COURSE",
                "value": "Python"
            },
            {
                "type": "MOODLE_FEATURE",
                "value": "course"
            }
        ]
    },
    {
        "text": "Where can I view my attendance?",
        "expected_entities": [
            {
                "type": "MOODLE_FEATURE",
                "value": "attendance"
            }
        ]
    },
    {
        "text": "I am not receiving course notifications",
        "expected_entities": [
            {
                "type": "MOODLE_FEATURE",
                "value": "notification"
            },
            {
                "type": "MOODLE_FEATURE",
                "value": "course"
            }
        ]
    },
    {
        "text": "رقم جوالي 0501234567 ولا أستطيع الدخول",
        "expected_entities": [
            {
                "type": "PERSONAL_DATA",
                "value": "<PHONE>"
            },
            {
                "type": "MOODLE_FEATURE",
                "value": "login"
            }
        ]
    }
]


output_folder = Path("data/test")
output_folder.mkdir(
    parents=True,
    exist_ok=True
)

output_file = (
    output_folder
    / "entity_test.json"
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        test_cases,
        file,
        ensure_ascii=False,
        indent=4
    )

print("Entity test dataset created")
print("Test cases:", len(test_cases))
print("File:", output_file)