from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail


def enviar_email_reativacao(usuario):
    """
    Envia um e-mail de reativação para o usuário fornecido.
    :param usuario: Um objeto User que representa o usuário.
    """
    
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(usuario)
    link = f"http://127.0.0.1:8000/reativar/{usuario.pk}/{token}"

    assunto = 'Reative sua conta'
    
    # Mensagem simples
    mensagem = (
        f"Olá, {usuario.first_name}! 👋\n"
        f"Clique neste link para reativar sua conta.\n"
        f"Caso não esteja esperando por esse e-mail, basta ignorá-lo 😉"
        f"Atenciosamente,\n"
        f"Equipe Voculary"
    )

    # Mensagem formatada em HTML
    mensagem_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; font-size: 14px; color: black;">
            <p>Olá, <strong>{usuario.first_name}</strong>! 👋</p>
            <p>Clique neste <a href="{link}">link</a> para reativar sua conta.</p>
            <p>Caso não esteja esperando por este e-mail, basta ignorá-lo. 😉</p>
            <p>Atenciosamente,</p>
            <p><strong>Equipe Voculary</strong></p>
        </body>
    </html>
    """
    
    remetente = 'voculary.projeto@gmail.com'
    destinatarios = [usuario.email]

    send_mail(assunto, mensagem, remetente, destinatarios, fail_silently=False, html_message=mensagem_html)