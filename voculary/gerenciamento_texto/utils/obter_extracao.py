import datetime
import io
import os

import requests
from django.contrib import messages
from django.core.cache import cache
from django.utils import timezone

from ..utils import extrair_texto


def obter_extracao(form, request):
    """
    Obter texto.
    :param form:
    :param request:
    """
    imagem = form.instance
    imagem.usuario = request.user
    imagem_content = None
    texto = None
    idioma = None

    try:
        if form.cleaned_data['url']:
            url = form.cleaned_data['url']
            nome_arquivo = os.path.basename(url)
            response = requests.get(url)
            if response.status_code == 200:
                imagem_content = response.content
                imagem_object = io.BytesIO(imagem_content)
                inicio_tempo = datetime.datetime.now(tz=timezone.utc)
                texto, idioma = extrair_texto(imagem_object)
                fim_tempo = datetime.datetime.now(tz=timezone.utc)

        else:
            imagem_content = form.cleaned_data['arquivo'].read()
            inicio_tempo = datetime.datetime.now(tz=timezone.utc)
            texto, idioma = extrair_texto(io.BytesIO(imagem_content))
            fim_tempo = datetime.datetime.now(tz=timezone.utc)
            lista = []
            for f in request.FILES.getlist('arquivo'):
                nome_arquivo = f.name
                lista.append(nome_arquivo)

            nome_arquivo = lista[0]

        fim_tempo = datetime.datetime.now(tz=timezone.utc)
        tempo_processamento = (fim_tempo - inicio_tempo).seconds

        cache.set(f"{request.user.id}_imagem", imagem_content, 3600)
        return imagem_content, nome_arquivo, texto, tempo_processamento, idioma
    except Exception as e:
        print(e)  
        messages.error(request, f'Puxa, parece que não foi possível extrair o texto. Tente novamente com outra imagem.')
        return None, None, None, None, None  