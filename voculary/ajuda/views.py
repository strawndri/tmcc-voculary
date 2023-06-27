from django.shortcuts import render

def ajuda(request):
    return render(request, 'ajuda/index.html')