import re

def extract_answers(quiz_text):

    answers = re.findall(
        r'Answer:\s*([A-D])',
        quiz_text,
        re.IGNORECASE
    )

    return answers


def parse_quiz(quiz_text):

    questions = []

    pattern = r"(Q\d+\..*?)(?=Q\d+\.|$)"

    matches = re.findall(
        pattern,
        quiz_text,
        re.DOTALL
    )

    for match in matches:

        question_text = match.strip()

        question_text = re.sub(
            r'Answer:\s*[A-D]',
            '',
            question_text,
            flags=re.IGNORECASE
        )

        questions.append(question_text)

    return questions