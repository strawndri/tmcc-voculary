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
    mensagem = (
        f"Olá, {usuario.first_name}!\n"
        f"Clique no link abaixo para reativar sua conta:\n{link}\n\n"
        f"Atenciosamente,\n"
        f"Equipe Voculary"
    )
    remetente = 'voculary.projeto@gmail.com'
    destinatarios = [usuario.email]

    send_mail(assunto, mensagem, remetente, destinatarios, fail_silently=False)