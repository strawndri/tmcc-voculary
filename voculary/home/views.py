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


def enviar_email_contato_view(request):
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
        
        # Mensagem simples
        mensagem = (
            f"De: {remetente}\n"
            f"Mensagem:\n{mensagem_usuario}"
        )

        # Mensagem formatada em HTML
        mensagem_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; font-size: 14px; color: black;">
                <p><strong>De:</strong> {remetente}</p>
                <hr>
                <p>{mensagem_usuario}</p>
            </body>
        </html>
        """

        # Envia o e-mail.
        send_mail(assunto, mensagem, '', destinatarios, fail_silently=False, html_message=mensagem_html)
        
        return redirect('home')