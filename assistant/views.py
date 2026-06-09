from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import UploadDocumentForm
from .models import UploadedDocument, QuizResult
from .gemini_utils import generate_summary
from .voice_utils import extract_pdf_text
from .utils import extract_answers, parse_quiz
import re

def home(request):
    return render(request, 'home.html')


def register_view(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'register.html', {'form': form})


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(
            request,
            'login.html',
            {'error': 'Invalid Username or Password'}
        )

    return render(request, 'login.html')

def dashboard(request):

    total_documents = UploadedDocument.objects.count()

    total_quizzes = QuizResult.objects.count()

    average_score = 0
    highest_score = 0

    if total_quizzes > 0:

        average_score = round(
            sum(
                result.percentage
                for result in QuizResult.objects.all()
            ) / total_quizzes,
            2
        )

        highest_score = max(
            result.percentage
            for result in QuizResult.objects.all()
        )

    return render(
        request,
        'dashboard.html',
        {
            'total_documents': total_documents,
            'total_quizzes': total_quizzes,
            'average_score': average_score,
            'highest_score': highest_score,
        }
    )


def upload_document(request):

    if request.method == "POST":

        form = UploadDocumentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            document = form.save()

            pdf_text = extract_pdf_text(
                document.document.path
            )

            from .quiz_utils import generate_quiz

            try:
                summary = generate_summary(
                    pdf_text[:10000]
                )
            except Exception as e:
                summary = f"Summary Error: {str(e)}"

            try:
                quiz = generate_quiz(
                    pdf_text[:10000]
                )
            except Exception as e:
                quiz = f"Quiz Error: {str(e)}"

            document.summary = summary
            document.quiz = quiz
            document.save()

            return redirect('upload')

    else:

        form = UploadDocumentForm()

    documents = UploadedDocument.objects.all()
    
    return render(
        request,
        "upload.html",
        {
            "form": form,
            "documents": documents
        }
    )


def quiz_page(request):

    documents = UploadedDocument.objects.all().order_by('-uploaded_at')

    score = None
    percentage = None

    for doc in documents:

        if doc.quiz:

            doc.parsed_questions = parse_quiz(
                doc.quiz
            )

    if request.method == "POST":

        doc_id = request.POST.get("doc_id")

        document = UploadedDocument.objects.get(
            id=doc_id
        )

        correct_answers = extract_answers(
            document.quiz
        )

        user_answers = [
            request.POST.get("q1"),
            request.POST.get("q2"),
            request.POST.get("q3"),
            request.POST.get("q4"),
            request.POST.get("q5"),
        ]

        score = 0

        for user, correct in zip(
            user_answers,
            correct_answers
        ):
            if user == correct:
                score += 1

        percentage = round(
            (score / len(correct_answers)) * 100,
            2
        )
        QuizResult.objects.create(
          document=document,
          score=score,
          percentage=percentage
        )

    return render(
        request,
        "quiz.html",
        {
            "documents": documents,
            "score": score,
            "percentage": percentage,
        }
    )

def summary_page(request):

    documents = UploadedDocument.objects.all().order_by('-uploaded_at')

    return render(
        request,
        'summary.html',
        {
            'documents': documents
        }
    )


def profile_page(request):
    return render(request, 'profile.html')

def quiz_results(request):

    results = QuizResult.objects.all().order_by(
        '-attempted_at'
    )

    return render(
        request,
        'quiz_results.html',
        {
            'results': results
        }
    )