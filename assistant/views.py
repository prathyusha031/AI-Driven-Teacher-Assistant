from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import UploadDocumentForm
from .models import UploadedDocument
from .gemini_utils import generate_summary
from .voice_utils import extract_pdf_text


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
    return render(request, 'dashboard.html')


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

    score = None

    if request.method == "POST":
        score = request.POST.get("score")

    documents = UploadedDocument.objects.all().order_by('-uploaded_at')

    return render(
        request,
        'quiz.html',
        {
            'documents': documents,
            'score': score
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