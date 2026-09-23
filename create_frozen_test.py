from pathlib import Path
import hashlib
import pandas as pd

from src.moodleguide.preprocessing import preprocess_text


records = [
    ("نسيت بيانات الدخول إلى المنصة", "ar", "student", "login_access"),
    ("حسابي مقفل بعد عدة محاولات", "ar", "instructor", "login_access"),
    ("Moodle rejects my username and password", "en", "student", "login_access"),

    ("اختفت مادة البرمجة من الصفحة الرئيسية", "ar", "student", "course_enrollment"),
    ("أريد تسجيل مجموعة جديدة في المقرر", "ar", "instructor", "course_enrollment"),
    ("A registered course is missing from my dashboard", "en", "student", "course_enrollment"),

    ("رفعت الملف ولكن حالة الواجب ما زالت مسودة", "ar", "student", "assignment"),
    ("أريد تمديد موعد تسليم التكليف", "ar", "instructor", "assignment"),
    ("Moodle will not accept my assignment file", "en", "student", "assignment"),

    ("انتهى الوقت قبل حفظ إجابات الاختبار", "ar", "student", "quiz_exam"),
    ("كيف أحدد عدد محاولات الاختبار؟", "ar", "instructor", "quiz_exam"),
    ("I need to import questions into the quiz", "en", "instructor", "quiz_exam"),

    ("نتيجتي تظهر بصفر رغم تسليم النشاط", "ar", "student", "grades"),
    ("كيف أعدّل درجة طالب يدويًا؟", "ar", "instructor", "grades"),
    ("Students cannot see their final marks", "en", "instructor", "grades"),

    ("ملف المحاضرة لا يعمل بعد تنزيله", "ar", "student", "course_content"),
    ("كيف أخفي المحاضرة حتى الأسبوع القادم؟", "ar", "instructor", "course_content"),
    ("I want to add a video to the course page", "en", "instructor", "course_content"),

    ("تم تسجيلي غائبًا رغم حضوري", "ar", "student", "attendance"),
    ("أحتاج إلى تصحيح سجل الحضور", "ar", "instructor", "attendance"),
    ("Where can I review my attendance record?", "en", "student", "attendance"),

    ("لا تصلني تنبيهات الواجبات الجديدة", "ar", "student", "notifications"),
    ("كيف أرسل رسالة لجميع المسجلين؟", "ar", "instructor", "notifications"),
    ("Course announcements are not reaching my email", "en", "student", "notifications"),

    ("رابط المحاضرة المباشرة يعطيني صفحة فارغة", "ar", "student", "virtual_class"),
    ("كيف أحدد موعد الفصل الافتراضي؟", "ar", "instructor", "virtual_class"),
    ("The online session has no join button", "en", "student", "virtual_class"),

    ("تتوقف الصفحة عند الضغط على حفظ", "ar", "instructor", "technical_problem"),
    ("يظهر خطأ غير معروف عند فتح النشاط", "ar", "student", "technical_problem"),
    ("Moodle signs me out whenever I open the course", "en", "student", "technical_problem")
]


df = pd.DataFrame(
    records,
    columns=[
        "text",
        "language",
        "user_role",
        "topic"
    ]
)

df.insert(0, "id", range(1, len(df) + 1))

df["processed_text"] = df.apply(
    lambda row: preprocess_text(
        row["text"],
        row["language"]
    ),
    axis=1
)

output_folder = Path("data/test")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "frozen_test.csv"

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

file_hash = hashlib.sha256(
    output_file.read_bytes()
).hexdigest()

manifest_file = output_folder / "frozen_test_manifest.txt"

manifest_file.write_text(
    f"file=frozen_test.csv\n"
    f"records={len(df)}\n"
    f"sha256={file_hash}\n",
    encoding="utf-8"
)

print("Frozen test set created")
print("Records:", len(df))
print("File:", output_file)
print("SHA-256:", file_hash)
print("\nDo not use this file for training.")