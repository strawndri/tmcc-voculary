from django import forms
from .models import Image

class UploadImagemForm(forms.ModelForm):
    """
    Formulário para o upload de imagens.
    
    Este formulário permite que os usuários façam upload de uma imagem diretamente
    ou forneçam uma URL de onde a imagem pode ser baixada.
    """
    
    # Campo para upload direto de imagens.
    arquivo = forms.ImageField(
        label='Imagem',
        required=False, 
        widget=forms.ClearableFileInput(attrs={'class': 'imagem input-imagem'}) 
    )

    # Campo para fornecer uma URL de imagem.
    url = forms.URLField(
        label='URL',
        required=False, 
        widget=forms.TextInput(attrs={'class': 'url input-imagem'})
    )

    class Meta:
        model = Image
        fields = ['arquivo', 'url'] 
