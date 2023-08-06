from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from home.models import Imagem, ArquivoDigitalizado

@login_required(login_url='/login')
def meus_arquivos(request):

    imagens = Imagem.objects.all()
    textos = ArquivoDigitalizado.objects.all()

    # paginação
    paginator = Paginator(imagens, 5)
    page = request.GET.get('page')
    imagens = paginator.get_page(page)

    return render(request, 'meus_arquivos/index.html', {'imagens': imagens})