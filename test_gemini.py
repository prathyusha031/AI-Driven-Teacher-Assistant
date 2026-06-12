from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

print("KEY =", key)

genai.configure(api_key=key)

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content("Say Hello")

print(response.text)