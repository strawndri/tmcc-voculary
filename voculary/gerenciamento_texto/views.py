import base64

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import UploadImagemForm
from .models import DigitizedText
from .utils import obter_extracao, salvar


@login_required(login_url='/login')
def geracao_texto_view(request):
    """
    """
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
                imagem_model = salvar(imagem_data, nome_arquivo, texto, tempo_processamento, idioma, request) 
                return redirect('/gerar-textos')

    else:
        cache.delete(cache_key)
        imagem_data, texto = None, None

    textos = DigitizedText.objects.select_related('image').order_by('-creation_date').filter(user=request.user, is_active=True)[:4]

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


@login_required(login_url='/login')
def meus_textos_view(request):
    """
    """
    order = request.GET.get('order', 'name_asc')  # 'name_asc' é o padrão

    ordering_map = {
        "name_asc": "name",
        "name_desc": "-name",
        "date_asc": "creation_date",
        "date_desc": "-creation_date"
    }

    order_by = ordering_map.get(order, 'name')
    textos = DigitizedText.objects.select_related('image').filter(user=request.user, is_active=True).order_by(order_by)

    if len(textos) == 0:
        mensagem = 'Puxa! Parece que você ainda não salvou nenhum texto.'
        return render(request, 'gerenciamento_texto/aviso.html', {'mensagem': mensagem})
    else:
        paginator = Paginator(textos, 10)
        page = request.GET.get('page')
        paginados = paginator.get_page(page)

        return render(request, 'gerenciamento_texto/meus_textos.html', {'paginados': paginados})
        

def obter_info_texto_view(request, id_imagem):
    """"""
    texto = DigitizedText.objects.get(image__image_id=id_imagem)

    data = {
        'nome': texto.name,
        'data_geracao': texto.creation_date.strftime('%d/%m/%Y'),
        'imagem_url': texto.image.file.url,
        'texto': texto.text
    }
    
    return JsonResponse(data)


@require_POST
def desativar_texto_view(request, texto_id):
    """"""
    print(id)
    try:
        texto = DigitizedText.objects.get(image_id=texto_id) 
        
        texto.is_active = False
        texto.save()

        if texto.image:  
            imagem = texto.image
            imagem.is_active = False
            imagem.save()

        messages.success(request, 'Texto excluído com sucesso!')
        return JsonResponse({"success": True, "message": "Texto excluído com sucesso!"})
    except Exception as e:
        print(e)
        return JsonResponse({"success": False, "message": "Ocorreu um erro ao tentar excluir o texto."})


def alterar_nome_texto_view(request, texto_id):
    """"""
    if request.method == 'POST':
        novo_nome = request.POST.get('novo_nome')
        texto = DigitizedText.objects.get(image_id=texto_id)
        
        if novo_nome == texto.name:
            return JsonResponse({'success': True})

        elif novo_nome == '':
            novo_nome = 'Sem título'
            texto.name = novo_nome
            texto.save()
            return JsonResponse({'success': True})
        else:
        
            texto.name = novo_nome
            texto.save()
            
            return JsonResponse({'success': True, 'message_type': 'success', 'message': 'Nome atualizado com sucesso!'})

    return JsonResponse({'success': False})
