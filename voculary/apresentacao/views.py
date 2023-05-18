from django.shortcuts import render

def apresentacao(request):
    return render(request, 'apresentacao/index.html')