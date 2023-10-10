from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from usuario.forms import LoginForms, CadastroForms, PerfilForms, PerfilSenhaForms
from usuario.models import User

from datetime import datetime

def CadastroView(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

        if form.is_valid():
           
            primeiro_nome = form['primeiro_nome'].value()
            ultimo_nome = form['ultimo_nome'].value()
            email = form['email'].value()
            senha = form['senha_1'].value()

            if User.objects.filter(email=email, is_active=True).exists():
                messages.error(request, 'Ops, parece que este e-mail já existe! Tente novamente.')
                return redirect('cadastro')
            
            usuario = User.objects.create_user(
                first_name = primeiro_nome,
                last_name = ultimo_nome,
                email = email,
                password = senha
            )

            usuario.save()
            messages.success(request, f'Eba! O cadastro foi realizado com sucesso.')
            return redirect('login')

    return render(request, 'usuario/cadastro.html', {'form': form})

def LoginView(request):
    form = LoginForms()

    if request.user.is_authenticated:
        return redirect('gerar-textos')

    elif request.method == 'POST':
        form = LoginForms(request.POST)


        if form.is_valid():
            email = form['email_login'].value()
            senha = form['senha'].value()

            Usuario = auth.get_user_model()
            
            
            usuario = Usuario.objects.filter(email=email).first()

            if usuario.is_active == False:
                enviar_email_reativacao(usuario)
            else:
                if usuario is not None and usuario.check_password(senha):
                    usuario.ultimo_login = datetime.now()
                    usuario.save()

                    auth.login(request, usuario)
                    messages.success(request, f'Olá, {usuario.first_name}! O login foi realizado com sucesso.')
                    return redirect('/gerar-textos')
                else:
                    messages.error(request, f'Oops! Usuário ou senha incorretos, tente novamente.')
                    return redirect('login')

    return render(request, 'usuario/login.html', {'form': form})

@login_required(login_url='/login')
def PerfilView(request):
    usuario = User.objects.get(id=request.user.id)

    form_gerais = PerfilForms(request.POST or None, instance=usuario)
    form_senha = PerfilSenhaForms(request.POST or None)

    if request.method == "POST":
        tipo_form = request.POST.get('tipo-form')

        if tipo_form == 'info_geral' and form_gerais.is_valid():
            form_gerais.save()
            messages.success(request, 'Dados atualizados com sucesso.')

        elif tipo_form == 'senha':
            if form_senha.is_valid():
                if usuario.check_password(form_senha.cleaned_data['senha_antiga']):
                    usuario.set_password(form_senha.cleaned_data['senha_nova'])
                    usuario.save()
                    messages.success(request, 'Senha atualizada com sucesso.')
                else:
                    messages.error(request, 'Senha antiga incorreta.')
            else:
                for error in form_senha.non_field_errors():
                    messages.error(request, error)
        
        elif tipo_form == 'excluir':
            try:
                usuario.is_active = False
                usuario.save()
            except:
                pass
            messages.success(request, 'Conta excluída com sucesso.')
            auth.logout(request)
            return redirect('/home')

    context = {
        'form_gerais': form_gerais,
        'form_senha': form_senha
    }

    return render(request, 'usuario/perfil.html', context)

@login_required(login_url='/login')
def LogoutView(request):
    messages.success(request, f'Até mais! O logout foi efetuado com sucesso.')
    auth.logout(request)
    return redirect('/home')

# reativação de conta
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail

def enviar_email_reativacao(user):
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    link = f"http://127.0.0.1:8000/reactivate/{user.pk}/{token}"
    send_mail(
        'Reativar sua conta',
        f'Clique no link para reativar sua conta: {link}',
        'voculary.projeto@example.com',
        [user.email],
        fail_silently=False,
    )

def reativar_conta(request, user_id, token):
    user = User.objects.get(pk=user_id)
    token_generator = PasswordResetTokenGenerator()
    if user and not user.is_active and token_generator.check_token(user, token):
        user.is_active = True
        user.save()