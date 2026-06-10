from django.db import models


class UploadedDocument(models.Model):

    title = models.CharField(max_length=200)

    document = models.FileField(
        upload_to='documents/'
    )

    summary = models.TextField(
        blank=True,
        null=True
    )

    quiz = models.TextField(
        blank=True,
        null=True
    )

    pdf_text = models.TextField(
        blank=True,
        null=True
    )

    score = models.IntegerField(default=0)

    percentage = models.FloatField(default=0)

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class QuizResult(models.Model):

    document = models.ForeignKey(
        UploadedDocument,
        on_delete=models.CASCADE,
        related_name="results"
    )

    score = models.IntegerField()

    percentage = models.FloatField()

    attempted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.document.title} - {self.score}/5"


class ChatHistory(models.Model):

    document = models.ForeignKey(
        UploadedDocument,
        on_delete=models.CASCADE
    )

    question = models.TextField()

    answer = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.question[:50]