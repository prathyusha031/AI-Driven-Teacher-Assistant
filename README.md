# AI-Driven Teacher Assistant

An AI-powered educational platform built using Django and Gemini AI that helps students learn more efficiently through document analysis, automatic summarization, intelligent quiz generation, performance evaluation, and AI-assisted learning support.

---

## Project Overview

AI-Driven Teacher Assistant enables students to upload study materials in PDF format and instantly receive:

- AI-generated summaries
- Automatically generated quizzes
- Quiz scoring and performance analysis
- AI-powered learning assistance
- Personalized study support

The platform is designed to reduce study time, improve understanding, and provide an interactive learning experience.

---

## Features

### User Authentication

- User Registration
- Login System
- Logout Functionality
- Profile Page

### Document Processing

- PDF Upload
- PDF Text Extraction
- Study Material Storage

### AI Summary Generation

- Automatic content summarization
- Easy-to-read study notes
- Quick revision support

### AI Quiz Generation

- Automatic MCQ creation
- Multiple-choice questions
- AI-generated answer keys

### Quiz Evaluation

- Quiz submission
- Automatic score calculation
- Percentage calculation
- Quiz performance tracking

### AI Learning Assistant

- AI-powered chatbot
- Question answering support
- Learning assistance from uploaded content

### Dashboard

- Centralized navigation
- Document management
- Learning progress overview

---

## Tech Stack

### Backend

- Python
- Django

### Artificial Intelligence

- Google Gemini AI

### Database

- SQLite

### Frontend

- HTML
- CSS
- Bootstrap 5
- JavaScript

### Other Libraries

- PyPDF2
- python-dotenv
- Google Generative AI SDK

---

## Project Structure

```text
AI-Driven-Teacher-Assistant/
│
├── ai_teacher/
├── assistant/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── quiz_utils.py
│   ├── chat_utils.py
│   ├── voice_utils.py
│   └── forms.py
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── summary.html
│   ├── quiz.html
│   ├── chat.html
│   ├── profile.html
│   └── logout.html
│
├── media/
├── static/
├── requirements.txt
├── manage.py
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/prathyusha031/AI-Driven-Teacher-Assistant.git
cd AI-Driven-Teacher-Assistant
```

### Create Virtual Environment

```bash
python -m venv env
```

### Activate Virtual Environment

Windows:

```bash
env\Scripts\activate
```

Linux / Mac:

```bash
source env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Start Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Application Workflow

1. User registers and logs in.
2. User uploads study material in PDF format.
3. System extracts text from the document.
4. Gemini AI generates a summary.
5. Gemini AI generates quiz questions.
6. User attempts the quiz.
7. System calculates score and percentage.
8. User interacts with the AI learning assistant.
9. Learning progress can be reviewed through the dashboard.

## Future Enhancements

- Voice-based learning assistant
- Multi-language support
- Personalized learning recommendations
- Advanced analytics dashboard
- Learning progress tracking
- Difficulty-based quiz generation
- Cloud deployment

---

## Learning Outcomes

This project helped in gaining practical experience in:

- Django Web Development
- Generative AI Integration
- Prompt Engineering
- PDF Processing
- Database Design
- User Authentication
- RESTful Application Design
- Full Stack Development

---

## Author

Bailapudi Prathyusha

B.Tech – Computer Science and Engineering (Data Science)

GitHub:
https://github.com/prathyusha031

LinkedIn:
(Add LinkedIn URL)

---

## License

MIT
