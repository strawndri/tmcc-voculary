import re

from django.core.mail import send_mail
from django.shortcuts import redirect, render


def home_view(request):
    """
    Renderiza a página inicial.
    :param request: HttpRequest
        Objeto de solicitação HTTP.
    """
    
    # Verifica se o caminho da requisição corresponde à página inicial.
    mostra_cabecalho_home = bool(re.match(r'^/?$|^/home/*?$', request.path))

    contexto = {
        'mostra_cabecalho_home': mostra_cabecalho_home,
        'esconde_barra_lateral': True  # Esconde a barra lateral no template
    }

    return render(request, 'home/index.html', contexto)


def enviar_email_reativacao_view(request):
    """
    Trata o envio de e-mail de reativação.
    Se o método da requisição for POST, a função extrai as informações
    do e-mail e envia a mensagem para os destinatários.
    
    :param request: HttpRequest
        Objeto de solicitação HTTP.
    """

    if request.method == "POST":
        assunto = 'Mensagem de Usuário da Voculary'
        mensagem_usuario = request.POST['mensagem']
        destinatarios = ['voculary.projeto@gmail.com']
        remetente = request.POST['email']
        
        # Formatação da mensagem que será enviada.
        mensagem_formatada = (
            f"De: {remetente}\n"
            f"Mensagem:\n{mensagem_usuario}"
        )

        # Envia o e-mail.
        send_mail(assunto, mensagem_formatada, '', destinatarios, fail_silently=False)
        
        return redirect('home')