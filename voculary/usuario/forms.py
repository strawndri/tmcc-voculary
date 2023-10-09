from django import forms
from django.contrib.auth.password_validation import validate_password

class LoginForms(forms.Form):
    email_login = forms.CharField(
        label='E-mail',
        required = True,
        max_length = 255,
    )

    senha = forms.CharField(
        label='Senha',
        required = True,
        max_length = 255,
        widget=forms.PasswordInput()
    )

class CadastroForms(forms.Form):
    primeiro_nome = forms.CharField(
        label='Primeino nome',
        required = True,
        max_length = 100,
        widget=forms.TextInput(
            attrs={'class':'nome'}
        )
    )

    ultimo_nome = forms.CharField(
        label='Último nome',
        required = True,
        max_length = 100,
        widget=forms.TextInput(
            attrs={'class':'nome'}
        )
    )

    email = forms.EmailField(
        label='Email',
        required = True,
        max_length = 255
    )

    senha_1 = forms.CharField(
        label='Senha',
        required = True,
        max_length = 255,
        widget=forms.PasswordInput(),
    )

    senha_2 = forms.CharField(
        label='Confirmação de senha',
        required = True,
        max_length = 255,
        widget=forms.PasswordInput()
    )

    def clean_senha_1(self):
        senha_1 = self.cleaned_data.get('senha_1')
        validate_password(senha_1)
        return senha_1

    def clean_senha_2(self):
        senha_1 = self.cleaned_data.get('senha_1')
        senha_2 = self.cleaned_data.get('senha_2')

        if senha_1 and senha_2:
            if senha_1 != senha_2:
                raise forms.ValidationError('Os dois campos de senha não correspondem.')
            else:
                return senha_2

from .models import User

class PerfilForms(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PerfilSenhaForms(forms.ModelForm):

    senha_antiga = forms.CharField(
        label='Senha antiga',
        required=True,
        max_length=255,
        widget=forms.PasswordInput()
    )

    senha_nova = forms.CharField(
        label='Senha nova',
        required=True,
        max_length=255,
        widget=forms.PasswordInput()
    )

    senha_nova_confirmacao = forms.CharField(
        label='Confirmação da senha nova',
        required=True,
        max_length=255,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = [] 

    def clean_senha_nova(self):
        senha_nova = self.cleaned_data.get('senha_nova')
        validate_password(senha_nova, self.instance) 
        return senha_nova

    def clean(self):
        cleaned_data = super().clean()
        senha_nova = cleaned_data.get('senha_nova')
        senha_nova_confirmacao = cleaned_data.get('senha_nova_confirmacao')
        
        if senha_nova != senha_nova_confirmacao:
            raise forms.ValidationError('Os dois campos de senha não correspondem.')

        return cleaned_data
