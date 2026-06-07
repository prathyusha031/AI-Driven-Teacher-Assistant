import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_quiz(text):

    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""
    Create 5 multiple-choice questions from the following text.

    Format:

    Q1.
    A)
    B)
    C)
    D)

    Answer:

    Text:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text