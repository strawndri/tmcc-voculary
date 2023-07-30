from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import UploadImagemForm

from .utils.extrair_texto import extrair_texto

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
            texto = extrair_texto(imagem.imagem.path)

    else:
        form = UploadImagemForm()
    
    context = {
        'form' : form,
        'texto': texto,   # Aqui passamos o texto como contexto
    }

    return render(request, 'home/index.html', context)