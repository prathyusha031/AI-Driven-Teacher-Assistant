from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import UploadDocumentForm
from .models import UploadedDocument, QuizResult, ChatHistory
from .gemini_utils import generate_summary
from .voice_utils import extract_pdf_text
from .utils import extract_answers, parse_quiz
import re
from django.contrib.auth import logout
from .chat_utils import ask_question
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.db.models import Avg, Max
from django.contrib.auth.decorators import login_required



def logout_view(request):

    logout(request)

    return render(
        request,
        "logout.html"
    )

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

from .models import UploadedDocument

@login_required
def dashboard(request):

    documents = UploadedDocument.objects.all()

    documents_count = UploadedDocument.objects.count()

    quiz_count = QuizResult.objects.count()

    chat_count = ChatHistory.objects.count()

    average_score = QuizResult.objects.aggregate(
        Avg("percentage")
    )["percentage__avg"] or 0

    highest_score = QuizResult.objects.aggregate(
        Max("percentage")
    )["percentage__max"] or 0

    return render(
        request,
        "dashboard.html",
        {
            "documents": documents,

            "documents_count": documents_count,

            "quiz_count": quiz_count,

            "chat_count": chat_count,

            "average_score": average_score,

            "highest_score": highest_score,
        }
    )

@login_required
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
            document.pdf_text = pdf_text
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


@login_required
def quiz_page(request):

    documents = UploadedDocument.objects.all().order_by(
        '-uploaded_at'
    )

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

        print("Correct Answers:", correct_answers)

        user_answers = [
            request.POST.get("q1"),
            request.POST.get("q2"),
            request.POST.get("q3"),
            request.POST.get("q4"),
            request.POST.get("q5"),
        ]

        print("User Answers:", user_answers)

        score = 0

        for user, correct in zip(
            user_answers,
            correct_answers
        ):

            if user == correct:
                score += 1

        if len(correct_answers) > 0:

            percentage = round(
                (score / len(correct_answers)) * 100,
                2
            )

        else:

            percentage = 0

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

@login_required
def summary_page(request):

    documents = UploadedDocument.objects.exclude(
        summary=""
    ).order_by("-uploaded_at")

    return render(
        request,
        "summary.html",
        {
            "documents": documents
        }
    )


@login_required
def profile_page(request):
    return render(request, 'profile.html')

@login_required
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

def start_learning(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    return redirect('login')

@login_required
def chat_page(request):

    documents = UploadedDocument.objects.all()

    answer = None

    if request.method == "POST":

        doc_id = request.POST.get("doc_id")
        question = request.POST.get("question")

        document = UploadedDocument.objects.get(
            id=doc_id
        )

        answer = ask_question(
            document.pdf_text,
            question
        )

        ChatHistory.objects.create(
            document=document,
            question=question,
            answer=answer
        )

    history = ChatHistory.objects.order_by(
        "-created_at"
    )[:10]

    return render(
        request,
        "chat.html",
        {
            "documents": documents,
            "answer": answer,
            "history": history
        }
    )

@login_required
def download_summary(request, doc_id):
    document = UploadedDocument.objects.get(
        id=doc_id
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = f'attachment; filename="{document.title}.pdf"'

    p = canvas.Canvas(response)

    y = 800

    p.drawString(
        50,
        y,
        f"Summary: {document.title}"
    )

    y -= 40

    for line in document.summary.split('\n'):

        p.drawString(
            50,
            y,
            line[:100]
        )

        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.save()

    return response