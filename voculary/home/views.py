from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import UploadImagemForm
from .models import ArquivoDigitalizado   # Importe seu modelo

from .utils.extrair_texto import extrair_texto
import time   # Importe a biblioteca time

@login_required(login_url='/login')
def home(request):
    texto = ''
    imagem = ''
    if request.method == 'POST':
        form = UploadImagemForm(request.POST, request.FILES)
        if form.is_valid():
            imagem = form.save(commit=False)
            imagem.usuario = request.user
            imagem.save()
            
            # Inicie o cronômetro para calcular o tempo de detecção
            inicio_tempo = time.time()

            # Extrair texto da imagem
            texto = extrair_texto(imagem.imagem.path)

            # Calcule o tempo que levou para extrair o texto
            tempo_processamento = time.time() - inicio_tempo
            
            # Crie uma nova entrada no modelo ArquivoDigitalizado
            arquivo_digitalizado = ArquivoDigitalizado(
                nome_arquivo=imagem.imagem.path,
                texto=texto,
                tempo_processamento=tempo_processamento,
                usuario=request.user,
                imagem=imagem
            )
            arquivo_digitalizado.save()

    else:
        form = UploadImagemForm()
    
    context = {
        'form' : form,
        'texto': texto
    }

    return render(request, 'home/index.html', context)
