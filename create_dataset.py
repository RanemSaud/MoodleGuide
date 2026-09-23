from pathlib import Path
import pandas as pd


data = [
    {
        "text": "لا أستطيع تسجيل الدخول إلى مودل",
        "language": "ar",
        "user_role": "student",
        "topic": "login_access",
        "sentiment": "negative",
        "answer": "استخدم خيار نسيت كلمة المرور أو تواصل مع الدعم التقني.",
        "route_to": "IT Support"
    },
    {
        "text": "كيف أعيد تعيين كلمة مرور حسابي؟",
        "language": "ar",
        "user_role": "student",
        "topic": "login_access",
        "sentiment": "neutral",
        "answer": "اضغط على نسيت كلمة المرور واتبع التعليمات المرسلة إلى بريدك.",
        "route_to": "IT Support"
    },
    {
        "text": "لا يظهر لي مقرر معالجة اللغة الطبيعية",
        "language": "ar",
        "user_role": "student",
        "topic": "course_enrollment",
        "sentiment": "negative",
        "answer": "تحقق من تسجيلك في المقرر، ثم تواصل مع القبول والتسجيل.",
        "route_to": "Registration Department"
    },
    {
        "text": "كيف أضيف طالبًا إلى مقرري؟",
        "language": "ar",
        "user_role": "instructor",
        "topic": "course_enrollment",
        "sentiment": "neutral",
        "answer": "افتح المشاركين ثم اختر تسجيل المستخدمين إذا كانت لديك الصلاحية.",
        "route_to": "eLearning Support"
    },
    {
        "text": "لا يظهر لي زر تسليم الواجب",
        "language": "ar",
        "user_role": "student",
        "topic": "assignment",
        "sentiment": "negative",
        "answer": "تحقق من موعد فتح الواجب وموعد الإغلاق، ثم تواصل مع مدرس المقرر.",
        "route_to": "Course Instructor"
    },
    {
        "text": "كيف أنشئ واجبًا جديدًا للطلاب؟",
        "language": "ar",
        "user_role": "instructor",
        "topic": "assignment",
        "sentiment": "neutral",
        "answer": "فعّل وضع التحرير ثم اختر إضافة نشاط من نوع واجب.",
        "route_to": "eLearning Support"
    },
    {
        "text": "تم إغلاق الاختبار قبل إكمال المحاولة",
        "language": "ar",
        "user_role": "student",
        "topic": "quiz_exam",
        "sentiment": "negative",
        "answer": "تحقق من وقت الاختبار ثم تواصل مباشرة مع مدرس المقرر.",
        "route_to": "Course Instructor"
    },
    {
        "text": "كيف أضيف أسئلة عشوائية من بنك الأسئلة؟",
        "language": "ar",
        "user_role": "instructor",
        "topic": "quiz_exam",
        "sentiment": "neutral",
        "answer": "افتح تحرير الاختبار ثم اختر إضافة سؤال عشوائي.",
        "route_to": "eLearning Support"
    },
    {
        "text": "أين أستطيع مشاهدة درجاتي؟",
        "language": "ar",
        "user_role": "student",
        "topic": "grades",
        "sentiment": "neutral",
        "answer": "افتح المقرر ثم اختر الدرجات من قائمة المقرر.",
        "route_to": "Course Instructor"
    },
    {
        "text": "درجات الاختبار غير ظاهرة للطلاب",
        "language": "ar",
        "user_role": "instructor",
        "topic": "grades",
        "sentiment": "negative",
        "answer": "راجع إعدادات خيارات المراجعة وإعدادات إظهار عنصر الدرجة.",
        "route_to": "eLearning Support"
    },
    {
        "text": "I cannot download the lecture file",
        "language": "en",
        "user_role": "student",
        "topic": "course_content",
        "sentiment": "negative",
        "answer": "Refresh the course page and verify that the resource is available.",
        "route_to": "eLearning Support"
    },
    {
        "text": "How can I upload lecture slides?",
        "language": "en",
        "user_role": "instructor",
        "topic": "course_content",
        "sentiment": "neutral",
        "answer": "Turn editing on and add a File resource to the course section.",
        "route_to": "eLearning Support"
    },
    {
        "text": "My attendance status is incorrect",
        "language": "en",
        "user_role": "student",
        "topic": "attendance",
        "sentiment": "negative",
        "answer": "Contact the course instructor and provide the attendance date.",
        "route_to": "Course Instructor"
    },
    {
        "text": "How do I record student attendance?",
        "language": "en",
        "user_role": "instructor",
        "topic": "attendance",
        "sentiment": "neutral",
        "answer": "Open the Attendance activity, create a session, and record attendance.",
        "route_to": "eLearning Support"
    },
    {
        "text": "I am not receiving course notifications",
        "language": "en",
        "user_role": "student",
        "topic": "notifications",
        "sentiment": "negative",
        "answer": "Check your Moodle notification preferences and registered email.",
        "route_to": "IT Support"
    },
    {
        "text": "How can I send an announcement to all students?",
        "language": "en",
        "user_role": "instructor",
        "topic": "notifications",
        "sentiment": "neutral",
        "answer": "Post the message in the course Announcements forum.",
        "route_to": "eLearning Support"
    },
    {
        "text": "The virtual classroom link does not open",
        "language": "en",
        "user_role": "student",
        "topic": "virtual_class",
        "sentiment": "negative",
        "answer": "Check the session time and allow pop-ups, then try the link again.",
        "route_to": "eLearning Support"
    },
    {
        "text": "How do I add a virtual class to my course?",
        "language": "en",
        "user_role": "instructor",
        "topic": "virtual_class",
        "sentiment": "neutral",
        "answer": "Turn editing on and add the available virtual classroom activity.",
        "route_to": "eLearning Support"
    },
    {
        "text": "The Moodle page keeps loading without opening",
        "language": "en",
        "user_role": "student",
        "topic": "technical_problem",
        "sentiment": "negative",
        "answer": "Clear the browser cache and try another supported browser.",
        "route_to": "IT Support"
    },
    {
        "text": "Students receive an error when opening the activity",
        "language": "en",
        "user_role": "instructor",
        "topic": "technical_problem",
        "sentiment": "negative",
        "answer": "Review the activity restrictions and contact e-learning support.",
        "route_to": "eLearning Support"
    }
]


df = pd.DataFrame(data)

df.insert(0, "id", range(1, len(df) + 1))

output_folder = Path("data/raw")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "moodle_inquiries.csv"

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("Dataset created successfully")
print("File:", output_file)
print("Number of records:", len(df))
print("\nTopics:")
print(df["topic"].value_counts())