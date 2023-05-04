from django.shortcuts import render

def estante(request):
    return render(request, 'estante/index.html')