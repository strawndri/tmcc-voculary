from django.shortcuts import render

def meus_arquivos(request):
    return render(request, 'meus_arquivos/index.html')