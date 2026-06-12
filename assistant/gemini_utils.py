import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def generate_summary(text):

    prompt = f"""
Summarize the following study material in a simple,
student-friendly format.

Use:
- Key Points
- Important Concepts
- Short Explanation

Study Material:
{text[:4000]}
"""

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:
     
     print("API KEY:", os.getenv("GEMINI_API_KEY"))
    
    return str(e)