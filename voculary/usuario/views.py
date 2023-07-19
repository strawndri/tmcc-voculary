from django.shortcuts import render, redirect

from usuario.forms import LoginForms, CadastroForms, PerfilForms

from django.contrib.auth.models import User
from django.contrib import auth, messages

def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

        if form.is_valid():
           
            primeiro_nome = form['primeiro_nome'].value()
            ultimo_nome = form['ultimo_nome'].value()
            email = form['email'].value()
            senha = form['senha_1'].value()

            if User.objects.filter(email='email').exists():
                messages.error(request, 'Usuário já existente.')
                return redirect('cadastro')
            
            usuario = User.objects.create_user(
                username = primeiro_nome + ultimo_nome,
                first_name = primeiro_nome,
                last_name = ultimo_nome,
                email = email,
                password = senha
            )

            usuario.save()
            messages.success(request, f'Boas vindas! O cadastro foi realizado com sucesso.')
            return redirect('login')

    return render(request, 'usuario/cadastro.html', {'form': form})

def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            email = form['email_login'].value()
            senha = form['senha'].value()

            User = auth.get_user_model()
            usuario = User.objects.filter(email=email).first()

            if usuario is not None and usuario.check_password(senha):
                auth.login(request, usuario)
                messages.success(request, f'Olá! O login foi realizado com sucesso.')
                return redirect('home')
            else:
                # messages.error(request, f'Oops! Usuário ou senha incorretos, tente novamente.')
                return redirect('login')

    return render(request, 'usuario/login.html', {'form': form})

def perfil(request):
    form = PerfilForms()

    if request.method == 'POST':
        form = PerfilForms(request.POST)

    return render(request, 'usuario/perfil.html', {'form': form})