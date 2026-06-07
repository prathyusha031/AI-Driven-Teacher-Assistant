from django import forms
from .models import UploadedDocument

class UploadDocumentForm(forms.ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ['title', 'document']