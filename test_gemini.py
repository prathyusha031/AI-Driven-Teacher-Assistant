from assistant.gemini_utils import generate_summary

sample_text = """
Artificial Intelligence is a branch of computer science that enables
machines to perform tasks that normally require human intelligence.
"""

summary = generate_summary(sample_text)

print(summary)