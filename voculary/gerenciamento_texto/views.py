import base64

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from gerenciamento_texto.forms import UploadImagemForm
from gerenciamento_texto.models import DigitizedText
from gerenciamento_texto.utils.obter_extracao import obter_extracao
from gerenciamento_texto.utils.salvar import salvar

@login_required(login_url='/login')
def geracao_texto_view(request):
    """
    Processa e exibe os resultados da extração de texto de uma imagem.
    :param request: HttpRequest
        Objeto de solicitação HTTP.
    """
    chave_cache = f"{request.user.id}_texto_e_imagem"
    dados_cache = cache.get(chave_cache, {})

    texto = dados_cache.get("texto", "")
    nome_arquivo = dados_cache.get("nome_arquivo")
    dados_imagem = dados_cache.get("imagem_data") 
    tempo_processamento = dados_cache.get("tempo_processamento")
    idioma = dados_cache.get("idioma")

    # Se o método for POST, processa o formulário
    if request.method == 'POST':
        formulario = UploadImagemForm(request.POST, request.FILES)

        if formulario.is_valid():
            if 'extrair' in request.POST:
                dados_imagem, nome_arquivo, texto, tempo_processamento, idioma = obter_extracao(formulario, request)
                cache.set(chave_cache, {
                    "texto": texto, 
                    "imagem_data": dados_imagem,  
                    "nome_arquivo": nome_arquivo,
                    "tempo_processamento": tempo_processamento,
                    "idioma": idioma
                }, 3600)

            elif 'salvar' in request.POST:
                salvar(dados_imagem, nome_arquivo, texto, tempo_processamento, idioma, request) 
                return redirect('/gerar-textos')

    else:
        cache.delete(chave_cache)
        dados_imagem, texto = None, None

    # Pega os últimos 4 textos gerados
    ultimos_textos = DigitizedText.objects.select_related('image').order_by('-creation_date').filter(user=request.user, is_active=True)[:4]

    # Converte imagem em base64 para visualização
    imagem_base64 = None
    if dados_imagem:
        imagem_base64 = f"data:image/jpeg;base64,{base64.b64encode(dados_imagem).decode('utf-8')}"

    formulario = UploadImagemForm()
    contexto = {
        'form': formulario,
        'texto': texto,
        'textos': ultimos_textos,
        'imagem_base64': imagem_base64
    }

    return render(request, 'gerenciamento_texto/gerar_textos.html', contexto)


@login_required(login_url='/login')
def meus_textos_view(request):
    """
    Exibe os textos gerados pelo usuário.
    :param request: HttpRequest
        Objeto de solicitação HTTP.
    """
    # Ordena os textos com base nos parâmetros fornecidos
    ordem = request.GET.get('order', 'nome_desc') 
    mapa_ordem = {
        "nome_asc": "name",
        "nome_desc": "-name",
        "data_asc": "creation_date",
        "data_desc": "-creation_date"
    }
    ordenado_por = mapa_ordem.get(ordem, '-name')

    busca = request.GET.get('busca', None)

    if busca:
        textos = DigitizedText.objects.select_related('image').filter(user=request.user, is_active=True, name__iregex=rf'.*{busca}.*').order_by(ordenado_por)
    else: 
        textos = DigitizedText.objects.select_related('image').filter(user=request.user, is_active=True).order_by(ordenado_por)

    # Se o usuário não tiver textos, exibe uma mensagem
    if not textos:
        mensagem = 'Puxa! Parece que você ainda não salvou nenhum texto.'
        return render(request, 'gerenciamento_texto/aviso.html', {'mensagem': mensagem})
    else:
        paginador = Paginator(textos, 10)
        pagina = request.GET.get('page')
        textos_paginados = paginador.get_page(pagina)

        return render(request, 'gerenciamento_texto/meus_textos.html', {'paginados': textos_paginados})


def obter_info_texto_view(request, id_imagem):
    """
    Retorna informações sobre um texto gerado a partir de uma imagem.
    :param request: HttpRequest
        Objeto de solicitação HTTP.
    :param id_imagem: int
        Chave primária da imagem selecionada.
    """
    texto = DigitizedText.objects.get(image__image_id=id_imagem)

    data = {
        'nome': texto.name,
        'data_geracao': texto.creation_date.strftime('%d/%m/%Y'),
        'imagem_url': texto.image.file.url,
        'texto': texto.text
    }
    
    return JsonResponse(data)


def desativar_textos_view(request):
    """
    Desativa múltiplos textos.
    """
    try:
        ids_imagem_str = request.POST.get('ids_imagem', '')  # Obtém a string de IDs (pode ser uma string vazia se não houver IDs)
        ids_imagem = [int(id) for id in ids_imagem_str.split(',') if id]

        for id in ids_imagem:
            texto = get_object_or_404(DigitizedText, image_id=id)
            texto.is_active = False
            texto.save()
            
            # Se o texto estiver associado a uma imagem, desative também a imagem
            if texto.image:
                imagem = texto.image
                imagem.is_active = False
                imagem.save()
        
        messages.success(request, f'{len(ids_imagem)} texto(s) excluído(s) com sucesso!')
        return JsonResponse({"success": True, "message": f'Texto(s) excluído(s) com sucesso!'})
    except Exception as e:
        return JsonResponse({"success": False, "message": "Ocorreu um erro ao tentar excluir os textos."})


def alterar_nome_texto_view(request, id_imagem):
    """
    Altera o nome de um texto específico.
    :param request: HttpRequest
        Objeto de solicitação HTTP.
    :param id_imagem: int
        Chave primária da imagem selecionada.
    """
    if request.method == 'POST':
        novo_nome = request.POST.get('novo_nome')
        texto = DigitizedText.objects.get(image_id=id_imagem)
        
        # Verifica se o nome é válido e salva
        if novo_nome == texto.name:
            return JsonResponse({'success': True})
        elif not novo_nome:
            texto.name = 'Sem título'
        else:
            texto.name = novo_nome
        
        texto.save()
        return JsonResponse({'success': True, 'message_type': 'success', 'message': 'Nome atualizado com sucesso!'})

    return JsonResponse({'success': False})