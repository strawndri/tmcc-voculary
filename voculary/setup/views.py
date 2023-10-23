from django.shortcuts import render

def erro_404(request, exception):

    context = {
        'erro_404': True
    }

    return render(request, '404.html', status=404, context=context)