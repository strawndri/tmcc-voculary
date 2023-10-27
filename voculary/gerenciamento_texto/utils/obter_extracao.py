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
    Obtém o texto extraído de uma imagem.

    :param form: Form
        Formulário contendo os dados da requisição.
    :param request: HttpRequest
        Objeto de solicitação HTTP.
    
    :return: tuple
        Imagem, nome do arquivo, texto extraído, tempo de processamento e idioma.
    """
    
    imagem = form.instance
    imagem.usuario = request.user
    conteudo_imagem = None
    texto = None
    idioma = None

    try:
        # Se uma URL foi fornecida no formulário.
        if form.cleaned_data['url']:
            url = form.cleaned_data['url']
            nome_arquivo = os.path.basename(url)
            resposta = requests.get(url)
            
            # Se a resposta da requisição foi bem-sucedida.
            if resposta.status_code == 200:
                conteudo_imagem = resposta.content
                objeto_imagem = io.BytesIO(conteudo_imagem)
                
                # Calcula o tempo de extração do texto.
                inicio_tempo = datetime.datetime.now(tz=timezone.utc)
                texto, idioma = extrair_texto(objeto_imagem)
                fim_tempo = datetime.datetime.now(tz=timezone.utc)
        else:
            # Se uma imagem foi enviada.
            conteudo_imagem = form.cleaned_data['arquivo'].read()
            inicio_tempo = datetime.datetime.now(tz=timezone.utc)
            texto, idioma = extrair_texto(io.BytesIO(conteudo_imagem))
            fim_tempo = datetime.datetime.now(tz=timezone.utc)
            
            lista_arquivos = []
            for arquivo in request.FILES.getlist('arquivo'):
                lista_arquivos.append(arquivo.name)

            nome_arquivo = lista_arquivos[0]

        # Calcula o tempo total de processamento/OCR da imagem.
        tempo_processamento = (fim_tempo - inicio_tempo).seconds

        # Armazena a imagem no cache por 1 hora.
        cache.set(f"{request.user.id}_imagem", conteudo_imagem, 3600)
        
        return conteudo_imagem, nome_arquivo, texto, tempo_processamento, idioma

    # Caso não seja possível extrair o texto da imagem, é retornado uma mensagem de erro,
    except Exception as e:
        messages.error(request, 'Puxa, parece que não foi possível extrair o texto. Tente novamente com outra imagem.')
        return None, None, None, None, None