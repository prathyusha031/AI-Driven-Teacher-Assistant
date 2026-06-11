import os
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_quiz(text):

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

    prompt = f"""
Create exactly 5 multiple-choice questions from the following text.

Format strictly:

Q1.
Question

A) Option A
B) Option B
C) Option C
D) Option D

Answer: A

Q2.
Question

A) Option A
B) Option B
C) Option C
D) Option D

Answer: B

Continue until Q5.

Rules:
- Exactly 5 questions
- 4 options each
- Must include Answer line
- Answer format exactly:
Answer: A
Answer: B
Answer: C
Answer: D

Text:
{text[:4000]}
"""

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        print("QUIZ ERROR:", e)

        return (
            "Quiz generation unavailable. "
            "Gemini API quota exceeded."
        )