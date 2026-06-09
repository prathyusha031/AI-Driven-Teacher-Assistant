import re

def extract_answers(quiz_text):

    answers = re.findall(
        r"Answer:\s*([A-D])",
        quiz_text
    )

    return answers