from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.core.cache import cache
from django.utils import timezone

from .forms import UploadImagemForm
from .models import Imagem, TextoDigitalizado

from .utils.extrair_texto import extrair_texto

import datetime, time, os, requests

@login_required(login_url='/login')
def GeracaoTextoView(request):
    cache_key = f"{request.user.id}_texto_e_imagem"
    cached_data = cache.get(cache_key, {})

    texto = cached_data.get("texto", "")
    imagem = cached_data.get("imagem")
    tempo_processamento = cached_data.get("tempo_processamento")
    idioma = cached_data.get("idioma")

    form = UploadImagemForm()

    if request.method == 'POST':
        form = UploadImagemForm(request.POST, request.FILES)
        if form.is_valid():
            if 'extrair' in request.POST:
                imagem, texto, tempo_processamento, idioma = obter_extracao(form, request)

                cache.set(cache_key, {
                    "texto": texto, 
                    "imagem": imagem,
                    "tempo_processamento": tempo_processamento,
                    "idioma": idioma
                }, 3600)

            elif 'salvar' in request.POST:
                salvar(imagem, texto, tempo_processamento, idioma, request)
                cache.delete(cache_key)
    else:
        cache.delete(cache_key)
        imagem, texto = None, None

    textos = TextoDigitalizado.objects.select_related('imagem').order_by('-data_geracao').filter(usuario=request.user)[:4]

    context = {
        'form': form,
        'texto': texto,
        'textos': textos,
        'imagem_url': imagem.arquivo.url if imagem else None
    }

    return render(request, 'gerenciamento_texto/gerar_textos.html', context)

def obter_extracao(form, request):
    imagem = form.save(commit=False)
    imagem.usuario = request.user

    if form.cleaned_data['url']:
        url = form.cleaned_data['url']
        response = requests.get(url)
    
        if response.status_code == 200:
            nome_arquivo = os.path.basename(url)
            imagem_temporaria = ContentFile(response.content)
            imagem.arquivo.save(nome_arquivo, imagem_temporaria)
    imagem.save()
    
    inicio_tempo = datetime.datetime.now(tz=timezone.utc)
    texto, idioma = extrair_texto(imagem.arquivo.path)
    fim_tempo = datetime.datetime.now(tz=timezone.utc)
    tempo_processamento = (fim_tempo - inicio_tempo).seconds

    return imagem, texto, tempo_processamento, idioma
                

def salvar(imagem, texto, tempo_processamento, idioma, request):
    time.sleep(1)
    if not texto:
        messages.error(request, f'Puxa, parece que não foi possível extrair o texto. Tente novamente com outra imagem.')
    else:
        texto_digitalizado = TextoDigitalizado(
            nome=os.path.basename(imagem.arquivo.path),
            texto=texto,
            tempo_processamento=tempo_processamento,
            usuario=request.user,
            imagem=imagem,
            idioma=idioma,
            ativo=True,
        )
        texto_digitalizado.save()
        messages.success(request, f'Imagem salva com sucesso! Você pode visualizá-la indo em "Meus textos".')


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
        

from django.http import JsonResponse

def obter_info_texto(request, id_imagem):
    texto = TextoDigitalizado.objects.get(imagem__id_imagem=id_imagem)
    
    # Converte o objeto em um dicionário para ser retornado como JSON
    data = {
        'nome': texto.nome,
        'data_geracao': texto.data_geracao.strftime('%d/%m/%Y'),
        'imagem_url': texto.imagem.arquivo.url,
        'texto': texto.texto
    }
    
    return JsonResponse(data)

