from django.shortcuts import render, redirect

from usuario.forms import LoginForms, CadastroForms, PerfilForms

from usuario.models import CustomUser

from django.contrib.auth.decorators import login_required
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

            if CustomUser.objects.filter(email='email').exists():
                messages.error(request, 'Usuário já existente.')
                return redirect('cadastro')
            
            usuario = CustomUser.objects.create_user(
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

@login_required(login_url='/login')
def perfil(request):

    form = PerfilForms()

    if request.method == 'POST':
        form = PerfilForms(request.POST)

    return render(request, 'usuario/perfil.html', {'form': form})

@login_required(login_url='/login')
def logout(request):
    messages.success(request, f'Até mais! O logout foi efetuado com sucesso.')
    auth.logout(request)
    return redirect('/apresentacao')