from django import forms
from .models import Imagem

class UploadImagemForm(forms.ModelForm):
    arquivo = forms.ImageField(
        label='Imagem',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'imagem'})
    )

    url = forms.URLField(
        label='URL',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form__input'})
    )

    class Meta:
        model = Imagem
        fields = ['arquivo', 'url']
