from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from usuario.forms import LoginForms, CadastroForms, PerfilForms
from usuario.models import Usuario

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

            if Usuario.objects.filter(email=email).exists():
                messages.error(request, 'Ops, parece que este e-mail já existe! Tente novamente.')
                return redirect('cadastro')
            
            usuario = Usuario.objects.create_user(
                primeiro_nome = primeiro_nome,
                ultimo_nome = ultimo_nome,
                email = email,
                senha = senha
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

            if usuario is not None and usuario.check_password(senha):
                usuario.ultimo_login = datetime.now()
                usuario.save()

                auth.login(request, usuario)
                messages.success(request, f'Olá, {usuario.primeiro_nome}! O login foi realizado com sucesso.')
                return redirect('/gerar-textos')
            else:
                messages.error(request, f'Oops! Usuário ou senha incorretos, tente novamente.')
                return redirect('login')

    return render(request, 'usuario/login.html', {'form': form})

@login_required(login_url='/login')
def PerfilView(request):

    form = PerfilForms()

    if request.method == 'POST':
        form = PerfilForms(request.POST)

    return render(request, 'usuario/perfil.html', {'form': form})

@login_required(login_url='/login')
def LogoutView(request):
    messages.success(request, f'Até mais! O logout foi efetuado com sucesso.')
    auth.logout(request)
    return redirect('/home')