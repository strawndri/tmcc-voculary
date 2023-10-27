"""
Configuração WSGI para o projeto "setup".

Este arquivo expõe a chamada WSGI como uma variável de nível de módulo chamada "application".

Para obter mais informações sobre este arquivo, consulte:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

# Importa os módulos necessários
import os
from django.core.wsgi import get_wsgi_application

# Define o módulo de configurações padrão para o Django.
# Isso permite ao Django saber onde procurar as configurações quando o projeto for iniciado.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

# Cria a aplicação WSGI usando as configurações padrão do Django.
# Isso permite ao servidor WSGI servir o projeto Django.
application = get_wsgi_application()