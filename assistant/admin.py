from django.contrib import admin
from .models import UploadedDocument, QuizResult, ChatHistory

admin.site.register(UploadedDocument)
admin.site.register(QuizResult)
admin.site.register(ChatHistory)