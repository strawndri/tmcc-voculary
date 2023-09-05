from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import UploadImagemForm
from .models import Imagem, TextoDigitalizado

from .utils.extrair_texto import extrair_texto
import time

@login_required(login_url='/login')
def GeracaoTextoView(request):
    texto = ''
    imagem = ''
    if request.method == 'POST':
        form = UploadImagemForm(request.POST, request.FILES)
        if form.is_valid():
            imagem = form.save(commit=False)
            imagem.usuario = request.user
            imagem.save()
            
            inicio_tempo = time.time()
            texto, idioma = extrair_texto(imagem.arquivo.path)
            tempo_processamento = time.time() - inicio_tempo
            
            texto_digitalizado = TextoDigitalizado(
                nome=imagem.arquivo.path,
                texto=texto,
                tempo_processamento=tempo_processamento,
                usuario=request.user,
                imagem=imagem,
                idioma=idioma,
                ativo=True,
            )
            
            texto_digitalizado.save()

    else:
        form = UploadImagemForm()
    
    context = {
        'form' : form,
        'texto': texto
    }

    return render(request, 'gerenciamento_texto/gerar_textos.html', context)


@login_required(login_url='/login')
def MeusTextosView(request):

    imagens = Imagem.objects.all()
    textos = TextoDigitalizado.objects.all()

    # paginação
    paginator = Paginator(imagens, 5)
    page = request.GET.get('page')
    imagens = paginator.get_page(page)

    return render(request, 'gerenciamento_texto/meus_textos.html', {'imagens': imagens})
