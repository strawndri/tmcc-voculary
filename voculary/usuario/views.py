import re
from datetime import datetime

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from usuario.forms import (CadastroForms, LoginForms, PerfilForms,
                           PerfilSenhaForms)
from usuario.models import User
from gerenciamento_texto.models import DigitizedText

from .utils.enviar_email_reativacao import enviar_email_reativacao


def cadastro_view(request):
    """
    Permite que um novo usuário se cadastre no sistema.

    :param request: HttpRequest
        Objeto de solicitação HTTP.
    """
    
    # Se o usuário já estiver autenticado, ele é redirecionado para 'gerar-textos'
    if request.user.is_authenticated:
        return redirect('gerar-textos')

    # Inicialização do formulário de cadastro
    form = CadastroForms(request.POST or None)

    # Verifica se o formulário é válido
    if form.is_valid():
        dados_do_formulario = form.cleaned_data
        email = dados_do_formulario['email']

        # Verifica se já existe um usuário com o e-mail fornecido
        usuario = User.objects.filter(email=email).first()

        # Se o usuário existir e estiver inativo, informa ao usuário
        if usuario and not usuario.is_active:
            messages.info(request, 'Puxa, parece que esse e-mail já existe e foi desativado. Caso queira recuperá-lo, acesse a página de Login.')
            return redirect('login')
        elif usuario:
            messages.error(request, 'Ops, parece que este e-mail já existe! Tente novamente.')
            return redirect('cadastro')

        # Caso não exista, cria um novo usuário com os dados fornecidos
        User.objects.create_user(
            first_name=dados_do_formulario['primeiro_nome'],
            last_name=dados_do_formulario['ultimo_nome'],
            email=email,
            password=dados_do_formulario['senha_1']
        )

        messages.success(request, 'Eba! O cadastro foi realizado com sucesso.')
        return redirect('login')

    # Configura o contexto que será enviado para o template
    contexto = {
        'form': form,
        # Verifica se o caminho atual corresponde ao cadastro
        'mostra_cabecalho_usuario': bool(re.match(r'^/cadastro/*?$', request.path))
    }

    return render(request, 'usuario/cadastro.html', contexto)

def login_view(request):
    """
    Faz login do usuário no sistema, identificando se ele realmente possui uma conta 
    ou se é necessário reativá-la.

    :param request: HttpRequest
        Objeto de solicitação HTTP.
    """
    
    # Se o usuário já estiver autenticado, ele é redirecionado para 'gerar-textos'
    if request.user.is_authenticated:
        return redirect('gerar-textos')

    # Inicialização do formulário de login
    form = LoginForms(request.POST or None)
    modal_confirmacao_email = False

    # Trata a tentativa de login via POST
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        senha = form.cleaned_data['senha']
        
        # Busca o usuário pelo e-mail
        usuario = auth.get_user_model().objects.filter(email=email).first()

        # Verifica se o usuário existe e se a senha está correta
        if usuario and usuario.check_password(senha):
            # Se o usuário estiver inativo, envia um e-mail para reativação
            if not usuario.is_active:
                modal_confirmacao_email = True
                enviar_email_reativacao(usuario)
                messages.info(request, 'Puxa, parece que esse e-mail já existe e foi desativado. Caso queira reativá-lo, te enviamos um e-mail!')
                return redirect('login')
            else:
                usuario.ultimo_login = datetime.now()
                usuario.save()
                auth.login(request, usuario)
                messages.success(request, f'Olá, {usuario.first_name}! O login foi realizado com sucesso.')
                return redirect('gerar-textos')

        # Caso contrário, informa erro ao usuário
        messages.error(request, 'Oops! Usuário ou senha incorretos, tente novamente.')
        return redirect('login')

    # Configura o contexto para renderizar o template de login
    contexto = {
        'form': form,
        # Verifica se o caminho atual corresponde ao login
        'mostra_cabecalho_usuario': bool(re.match(r'^/login/*?$', request.path)),
        'modal_confirmacao_email': modal_confirmacao_email
    }

    return render(request, 'usuario/login.html', contexto)


@login_required(login_url='/login')
def perfil_view(request):
    """
    Permite que o usuário edite seu perfil, altere sua senha ou exclua sua conta.

    :param request: HttpRequest
        Objeto de solicitação HTTP.
    """
    
    # Obtém o usuário atual
    usuario_atual = User.objects.get(id=request.user.id)
    
    # Inicializa os formulários
    form_dados_gerais = PerfilForms(request.POST or None, instance=usuario_atual)
    form_alterar_senha = PerfilSenhaForms(request.POST or None)

    # Verifica se a requisição é do tipo POST e processa os formulários
    if request.method == "POST":
        tipo_de_formulario = request.POST.get('tipo-form')
        
        # Formulário de informações gerais
        if tipo_de_formulario == 'info_geral' and form_dados_gerais.is_valid():
            form_dados_gerais.save()
            messages.success(request, 'Dados atualizados com sucesso.')
            return JsonResponse({"success": True, "message": f'Dados atualizados com sucesso.'})

        # Formulário de alteração de senha
        elif tipo_de_formulario == 'senha':
            if form_alterar_senha.is_valid():
                print(form_alterar_senha)
                if usuario_atual.check_password(form_alterar_senha.cleaned_data['senha_antiga']):
                    usuario_atual.set_password(form_alterar_senha.cleaned_data['senha_nova'])
                    usuario_atual.save()
                    messages.success(request, 'Senha atualizada com sucesso.')
                    return JsonResponse({"success": True, "message": f'Senha atualizada com sucesso.'})
                else:
                    messages.error(request, 'Senha antiga incorreta.')
                    return JsonResponse({"success": False, "message": f'Senha antiga incorreta.'})
            else:
                for erro in form_alterar_senha.non_field_errors():
                    messages.error(request, erro)
                    return JsonResponse({"success": False, "message": 'Não foi possível atualizar a senha.'})

        # Opção de 'exclusão' de conta
        elif tipo_de_formulario == 'excluir':
            usuario_atual.is_active = False

            textos = DigitizedText.objects.filter(user=usuario_atual)

            for texto in textos:
                texto.is_active = False
                texto.save()
                
                # Se o texto estiver associado a uma imagem, desative também a imagem
                if texto.image:
                    imagem = texto.image
                    imagem.is_active = False
                    imagem.save()

            usuario_atual.save()
            
            messages.success(request, 'Conta excluída com sucesso.')
            auth.logout(request)
            return redirect('/home')

    # Configura o contexto para renderizar o template de perfil
    contexto = {
        'form_dados_gerais': form_dados_gerais,
        'form_alterar_senha': form_alterar_senha
    }

    return render(request, 'usuario/perfil.html', contexto)

def reativar_conta_view(request, id_usuario, token):
    """
    Realiza a reativação da conta de um usuário que antes a desativou.

    :param request: HttpRequest
        Objeto de solicitação HTTP.
    :param id_usuario: int
        ID do usuário que deseja reativar a conta.
    :param token: str
        Token de verificação para reativar a conta.
    """

    # Tentativa de obter o usuário pelo ID fornecido
    try:
        usuario = User.objects.get(pk=id_usuario)
    except User.DoesNotExist:
        usuario = None
    
    # Verifica se o usuário existe, está inativo e se o token fornecido é válido
    if usuario and not usuario.is_active and PasswordResetTokenGenerator().check_token(usuario, token):
        if usuario.is_admin or usuario.is_staff:
            messages.error(request, 'Administradores e staffs não podem ter usas contas reativadas.')
        else:
            usuario.is_active = True
            textos = DigitizedText.objects.filter(usuario=usuario)

            for texto in textos:
                texto.is_active = True
                texto.save()
                
                # Se o texto estiver associado a uma imagem, desative também a imagem
                if texto.image:
                    imagem = texto.image
                    imagem.is_active = True
                    imagem.save()

            usuario.save()

    return render(request, 'usuario/reativar_conta.html')

@login_required(login_url='/login')
def logout_view(request):
    """
    Faz logout do usuário atualmente autenticado e redireciona para a página inicial.

    :param request: HttpRequest
        Objeto de solicitação HTTP.
    """

    # Envia uma mensagem de sucesso
    messages.success(request, 'Até mais! O logout foi efetuado com sucesso.')
    
    # Realiza o logout
    auth.logout(request)

    # Redireciona para a página inicial
    return redirect('/home')