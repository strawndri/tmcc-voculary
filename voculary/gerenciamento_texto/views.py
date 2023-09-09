from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.utils import timezone

from .forms import UploadImagemForm
from .models import Imagem, TextoDigitalizado

from .utils.extrair_texto import extrair_texto

import datetime
import os
import requests

@login_required(login_url='/login')
def GeracaoTextoView(request):
    texto = ''
    imagem = ''
    if request.method == 'POST':
        form = UploadImagemForm(request.POST, request.FILES)
        if form.is_valid():
            imagem = form.save(commit=False)
            imagem.usuario = request.user

            if form.cleaned_data['url']:
                url = form.cleaned_data['url']
                response = requests.get(url)
            
                if response.status_code == 200:
                    nome_arquivo = os.path.basename(url)
                    imagem_temporaria = ContentFile(response.content)
                    imagem.arquivo.save(nome_arquivo, imagem_temporaria)

            nome_arquivo = os.path.basename(imagem.arquivo.path)
            imagem.save()
            
            inicio_tempo = datetime.datetime.now(tz=timezone.utc)
            texto, idioma = extrair_texto(imagem.arquivo.path)
            fim_tempo = datetime.datetime.now(tz=timezone.utc)
            tempo_processamento = (fim_tempo - inicio_tempo).seconds

            if texto:
                texto_digitalizado = TextoDigitalizado(
                    nome=nome_arquivo,
                    texto=texto,
                    tempo_processamento=tempo_processamento,
                    usuario=request.user,
                    imagem=imagem,
                    idioma=idioma,
                    ativo=True,
                )
                
                texto_digitalizado.save()
            else: 
                messages.error(request, f'Puxa, parece que não foi possível extrair o texto. Tente novamente com outra imagem.')

    else:
        form = UploadImagemForm()
    
    context = {
        'form' : form,
        'texto': texto
    }

    return render(request, 'gerenciamento_texto/gerar_textos.html', context)


@login_required(login_url='/login')
def MeusTextosView(request):

    textos = TextoDigitalizado.objects.select_related('imagem').filter(usuario=request.user)

    if len(textos) == 0:
        mensagem = 'Puxa! Parece que você ainda não salvou nenhum texto.'
        return render(request, 'partials/_aviso.html', {'mensagem': mensagem})
    else:
        paginator = Paginator(textos, 5)
        page = request.GET.get('page')
        paginados = paginator.get_page(page)

        return render(request, 'gerenciamento_texto/meus_textos.html', {'paginados': paginados})
