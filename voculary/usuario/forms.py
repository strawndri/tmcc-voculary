from django import forms

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
        widget=forms.PasswordInput()
    )

    senha_2 = forms.CharField(
        label='Confirmação de senha',
        required = True,
        max_length = 255,
        widget=forms.PasswordInput()
    )

    def clean_senha_2(self):
        senha_1 = self.cleaned_data.get('senha_1')
        senha_2 = self.cleaned_data.get('senha_2')

        if senha_1 and senha_2:
            if senha_1 != senha_2:
                raise forms.ValidationError('Oops! Parece que as senhas estão diferentes. Tente novamente.')
            else:
                return senha_2

from .models import Usuario

class PerfilForms(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['primeiro_nome', 'ultimo_nome', 'email']

    senha_antiga = forms.CharField(
        label='Senha antiga',
        required = True,
        max_length = 255,
        widget=forms.PasswordInput()
    )

    senha_nova = forms.CharField(
        label='Senha nova',
        required = True,
        max_length = 255,
        widget=forms.PasswordInput()
    )

    senha_nova_confirmacao = forms.CharField(
        label='Confirmação da senha nova',
        required = True,
        max_length = 255,
        widget=forms.PasswordInput()
    )