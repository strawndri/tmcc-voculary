from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.core.cache import cache
from django.utils import timezone

from .forms import UploadImagemForm
from .models import Imagem, TextoDigitalizado

from .utils.extrair_texto import extrair_texto

import datetime, time, os, io, requests
import base64

@login_required(login_url='/login')
def GeracaoTextoView(request):
    cache_key = f"{request.user.id}_texto_e_imagem"
    cached_data = cache.get(cache_key, {})

    texto = cached_data.get("texto", "")
    nome_arquivo = cached_data.get("nome_arquivo")
    imagem_data = cached_data.get("imagem_data") 
    tempo_processamento = cached_data.get("tempo_processamento")
    idioma = cached_data.get("idioma")

    if request.method == 'POST':
        form = UploadImagemForm(request.POST, request.FILES)

        if form.is_valid():
            if 'extrair' in request.POST:
                imagem_data, nome_arquivo, texto, tempo_processamento, idioma = obter_extracao(form, request)

                cache.set(cache_key, {
                    "texto": texto, 
                    "imagem_data": imagem_data,  
                    "nome_arquivo": nome_arquivo,
                    "tempo_processamento": tempo_processamento,
                    "idioma": idioma
                }, 3600)

            elif 'salvar' in request.POST:
                imagem_model_instance = salvar(imagem_data, nome_arquivo, texto, tempo_processamento, idioma, request) 
                return redirect('/gerar-textos')

    else:
        cache.delete(cache_key)
        imagem_data, texto = None, None

    textos = TextoDigitalizado.objects.select_related('imagem').order_by('-data_geracao').filter(usuario=request.user, ativo=True)[:4]

    imagem_base64 = None
    if imagem_data:
        imagem_base64 = f"data:image/jpeg;base64,{base64.b64encode(imagem_data).decode('utf-8')}"

    form = UploadImagemForm()
    context = {
        'form': form,
        'texto': texto,
        'textos': textos,
        'imagem_base64': imagem_base64
    }

    return render(request, 'gerenciamento_texto/gerar_textos.html', context)


import numpy as np
def obter_extracao(form, request):
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

def salvar(imagem, nome_arquivo, texto, tempo_processamento, idioma, request):
    try:
        time.sleep(1)
        imagem_content = cache.get(f"{request.user.id}_imagem")

        imagem = Imagem(usuario=request.user)  
        imagem.arquivo.save(nome_arquivo, ContentFile(imagem_content))
        imagem.save()
        
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
    except:
        messages.error(request, "Ocorreu um erro ao salvar a imagem.")


@login_required(login_url='/login')
def MeusTextosView(request):

    textos = TextoDigitalizado.objects.select_related('imagem').filter(usuario=request.user, ativo=True)

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
    
    data = {
        'nome': texto.nome,
        'data_geracao': texto.data_geracao.strftime('%d/%m/%Y'),
        'imagem_url': texto.imagem.arquivo.url,
        'texto': texto.texto
    }
    
    return JsonResponse(data)

from django.views.decorators.http import require_POST

@require_POST
def desativar_texto(request, texto_id):
    try:
        texto = TextoDigitalizado.objects.get(id=texto_id) 
        
        texto.ativo = False
        texto.save()

        if texto.imagem:  
            imagem = texto.imagem
            imagem.ativo = False
            imagem.save()

        messages.success(request, 'Texto excluído com sucesso!')
        return JsonResponse({"success": True, "message": "Texto excluído com sucesso!"})
    except Exception as e:
        print(e)
        return JsonResponse({"success": False, "message": "Ocorreu um erro ao tentar excluir o texto."})

from django.http import JsonResponse

def alterar_nome_texto(request, texto_id):
    if request.method == 'POST':
        novo_nome = request.POST.get('novo_nome')
        texto = TextoDigitalizado.objects.get(id=texto_id)
        
        # nome não foi modificado - manter!
        if novo_nome == texto.nome:
            return JsonResponse({'success': True})

        elif novo_nome == '':
            novo_nome = 'Sem título'
            texto.nome = novo_nome
            texto.save()
            return JsonResponse({'success': True})
        else:
        
            texto.nome = novo_nome
            texto.save()

            return JsonResponse({'success': True, 'message_type': 'success', 'message': 'Nome atualizado com sucesso!'})

    return JsonResponse({'success': False})
