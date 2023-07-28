from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import UploadImagemForm

@login_required(login_url='/login')
def home(request):
    if request.method == 'POST':
        form = UploadImagemForm(request.POST, request.FILES)
        if form.is_valid():
            imagem = form.save(commit=False)
            imagem.usuario = request.user
            imagem.save()

    else:
        form = UploadImagemForm()
    
    return render(request, 'home/index.html', {'form' : form})