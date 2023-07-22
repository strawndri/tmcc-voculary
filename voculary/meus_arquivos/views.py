from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def meus_arquivos(request):
    return render(request, 'meus_arquivos/index.html')