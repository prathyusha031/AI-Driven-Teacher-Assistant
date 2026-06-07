from django.db import models

class UploadedDocument(models.Model):
    title = models.CharField(max_length=200)
    document = models.FileField(upload_to='documents/')
    summary = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title