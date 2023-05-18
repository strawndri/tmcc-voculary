from django.shortcuts import render

from usuario.forms import LoginForms, CadastroForms, PerfilForms

def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

    return render(request, 'usuario/cadastro.html', {'form': form})

def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

    return render(request, 'usuario/login.html', {'form': form})

def perfil(request):
    form = PerfilForms()

    if request.method == 'POST':
        form = PerfilForms(request.POST)

    return render(request, 'usuario/perfil.html', {'form': form})