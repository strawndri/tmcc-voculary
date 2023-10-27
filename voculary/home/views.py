import re

from django.core.mail import send_mail
from django.shortcuts import redirect, render


def home_view(request):
    
    mostra_cabecalho_home = bool(re.match(r'^/?$|^/home/*?$', request.path))

    context = {
        'mostra_cabecalho_home': mostra_cabecalho_home,
        'esconde_barra_lateral': True
    }

    return render(request, 'home/index.html', context)


def enviar_email_reativacao_view(request):
    if request.method == "POST":

        assunto = 'Mensagem de Usuário da Voculary'
        mensagem = request.POST['mensagem']
        destinatarios = ['voculary.projeto@gmail.com']
        remetente = request.POST['email']
        
        mensagem = (
        f"De: {remetente}\n"
        f"Mensagem:\n{mensagem}"
        )

        send_mail(assunto, mensagem, '', destinatarios, fail_silently=False)
        
        return redirect('home')