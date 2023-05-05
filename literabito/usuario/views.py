from django.shortcuts import render

from usuario.forms import LoginForms, CadastroForms

def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

    return render(request, 'usuario/cadastro.html', {'form': form})

def login(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

    return render(request, 'usuario/login.html', {'form': form})