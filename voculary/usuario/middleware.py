from django.http import HttpResponseRedirect
from django.urls import reverse

class AdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):  # Se o caminho começa com /admin/
            if not request.user.is_authenticated:  # Se o usuário não está logado
                return HttpResponseRedirect('/')  # Redireciona para a página inicial
            elif not request.user.is_staff:  # Se o usuário não tem permissões de staff
                return HttpResponseRedirect('/')  # Redireciona para a página inicial

        response = self.get_response(request)
        return response