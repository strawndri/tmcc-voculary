from django.shortcuts import render

def erro_404_view(request, exception):
    """
    Visualização renderizada quando a página acessada pelo usuário
    não for encontrada.

    :param request: HttpRequest
        Objeto de solicitação HTTP.
    :param exception: Exception
        Objeto de exceção levantado.
    :return: HttpResponse
        Resposta HTTP com a página de erro 404.
    """
    context = {
        'erro_404': True
    }

    return render(request, '404.html', status=404, context=context)