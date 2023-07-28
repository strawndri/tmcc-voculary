from django import forms
from .models import Imagem

class UploadImagemForm(forms.ModelForm):
    class Meta:
        model = Imagem
        fields = ['imagem']