import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Create model
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_summary(text):
    """
    Generate summary from extracted PDF text
    """

    prompt = f"""
    Summarize the following study material in a simple and student-friendly way.

    Study Material:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text