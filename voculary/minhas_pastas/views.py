from django.shortcuts import render

def minhas_pastas(request):
    return render(request, 'minhas_pastas/index.html')