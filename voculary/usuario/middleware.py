from django.http import HttpResponseRedirect
from django.urls import reverse


class AdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Se o caminho começa com /admin/
        if request.path.startswith(reverse('admin:index')):

            # Se o usuário não está logado
            if not request.user.is_authenticated:  
                return HttpResponseRedirect('/') 
            
            # Se o usuário não tem permissões de staff
            elif not request.user.is_staff:  
                return HttpResponseRedirect('/') 

        response = self.get_response(request)
        return response