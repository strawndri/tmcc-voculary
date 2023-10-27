import os
import time

from django.contrib import messages
from django.core.cache import cache
from django.core.files.base import ContentFile

from ..models import DigitizedText, Image


def salvar(imagem, nome_arquivo, texto, tempo_processamento, idioma, request):
    """
    Salva no banco de dados a imagem enviada pelo usuário
    e o texto gerado a partir desta imagem.
    :param imagem:
    :param nome_arquivo:
    :param texto:
    :param tempo_processamento:
    :param idioma:
    """
    try:
        time.sleep(1)
        imagem_content = cache.get(f"{request.user.id}_imagem")

        imagem = Image(user=request.user)  
        imagem.file.save(nome_arquivo, ContentFile(imagem_content))
        imagem.save()
        
        texto_digitalizado = DigitizedText(
            name=os.path.basename(imagem.file.path),
            text=texto,
            processing_time=tempo_processamento,
            user=request.user,
            image=imagem,
            language=idioma,
            is_active=True,
        )
        texto_digitalizado.save()
        messages.success(request, f'Imagem salva com sucesso! Você pode visualizá-la indo em "Meus textos".')
    except:
        messages.error(request, "Ocorreu um erro ao salvar a imagem.")