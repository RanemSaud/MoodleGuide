from src.moodleguide.preprocessing import preprocess_text


arabic_text = """
اسمي رنيم ورقمي الجامعي 202600224
ورقم جوالي 0501242830 وبريدي student@example.com
"""

result = preprocess_text(arabic_text, "ar")

print("Original:")
print(arabic_text)

print("\nProcessed:")
print(result)