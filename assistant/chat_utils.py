from .gemini_utils import model

def ask_question(notes, question):

    prompt = f"""
    You are an AI Teacher Assistant.

    Study Notes:
    {notes}

    Student Question:
    {question}

    Answer clearly and simply.
    """

    response = model.generate_content(prompt)

    return response.text