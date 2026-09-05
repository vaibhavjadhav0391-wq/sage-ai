from app.services.gemini_service import analyze_answer


result = analyze_answer(
    concept="Arrays",
    question="What is the first index of an array in Java?",
    student_answer="1"
)

print(result)