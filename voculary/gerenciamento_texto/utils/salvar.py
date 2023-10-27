import os
import time

from django.contrib import messages
from django.core.cache import cache
from django.core.files.base import ContentFile

from ..models import DigitizedText, Image


def salvar(imagem, nome_arquivo, texto, tempo_processamento, idioma, request):
    """
    Salva no banco de dados a imagem enviada pelo usuário e o texto gerado a partir desta imagem.
    
    :param imagem: ContentFile
        Imagem a ser salva.
    :param nome_arquivo: str
        Nome do arquivo da imagem.
    :param texto: str
        Texto extraído da imagem.
    :param tempo_processamento: float
        Tempo gasto para processar a imagem.
    :param idioma: str
        Idioma identificado na imagem.
    :param request: HttpRequest
        Objeto de solicitação HTTP.
    """
    
    # Adiciona um atraso para sincronizar operações
    time.sleep(1)
    
    # Busca a imagem no cache
    conteudo_imagem = cache.get(f"{request.user.id}_imagem")
    
    try:
        # Salva a imagem no banco de dados
        imagem_modelo = Image(user=request.user)  
        imagem_modelo.file.save(nome_arquivo, ContentFile(conteudo_imagem))
        imagem_modelo.save()

        # Salva o texto digitalizado associado à imagem no banco de dados
        texto_digitalizado = DigitizedText(
            name=os.path.basename(imagem_modelo.file.path),
            text=texto,
            processing_time=tempo_processamento,
            user=request.user,
            image=imagem_modelo,
            language=idioma,
            is_active=True,
        )
        texto_digitalizado.save()

        # Exibe uma mensagem de sucesso
        messages.success(request, 'Imagem salva com sucesso! Você pode visualizá-la indo em "Meus textos".')
    
    except:
        # Exibe uma mensagem de erro em caso de falha ao salvar
        messages.error(request, "Ocorreu um erro ao salvar a imagem.")