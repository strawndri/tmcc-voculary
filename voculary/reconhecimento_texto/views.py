from django.shortcuts import render

def reconhecimento_texto(request):
    return render(request, 'reconhecimento_texto/index.html')
