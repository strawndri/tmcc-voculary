"""
Configuração ASGI para o projeto 'setup'.

Expõe a aplicação ASGI como uma variável de nível de módulo chamada ``application``.

Para mais informações sobre este arquivo, consulte:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Define o módulo de configurações padrão para o Django. 
# 'setup.settings' é o local do arquivo de configurações deste projeto.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

# Obtém a aplicação ASGI padrão do Django.
application = get_asgi_application()
