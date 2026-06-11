import google.generativeai as genai
import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_quiz(text):

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

    prompt = f"""
Create exactly 5 multiple-choice questions from the following text.

Use this format strictly:

Q1.
Question text

A) Option A
B) Option B
C) Option C
D) Option D

Answer: C

Q2.
Question text

A) Option A
B) Option B
C) Option C
D) Option D

Answer: A

Continue until Q5.

Important Rules:
- Generate exactly 5 questions.
- Each question must have 4 options (A, B, C, D).
- Every question MUST include an answer line.
- Answer line format must be exactly:
Answer: A
or
Answer: B
or
Answer: C
or
Answer: D

Text:
{text}
"""

    response = model.generate_content(
        prompt
    )

    return response.text