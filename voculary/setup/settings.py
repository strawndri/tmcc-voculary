from pathlib import Path
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Chave secreta da aplicação
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuração de depuração - NÃO ative o modo de depuração em produção!
DEBUG = False

# Lista de hosts permitidos (neste exemplo, qualquer host é permitido)
ALLOWED_HOSTS = ['*']

# Definição das aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'usuario',
    'gerenciamento_texto',
]

# Middleware da aplicação
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'usuario.middleware.AdminMiddleware',
]

# URL raiz
ROOT_URLCONF = 'setup.urls'

# Configurações dos templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Pasta de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Caminho para a aplicação WSGI
WSGI_APPLICATION = 'setup.wsgi.application'

# Configurações do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'voculary'),
        'USER': os.environ.get('DB_USER', 'adminvocs'),
        'PASSWORD': os.environ.get('DB_PASS', 'Tmd#voculary23'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Definição de modelo de usuário personalizado
AUTH_USER_MODEL = 'usuario.User'

# Configuração de validadores de senha
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configurações de idioma e fuso horário
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Configurações de arquivos estáticos e mídia
STATIC_URL = 'static/'
MEDIA_URL = '/media/'

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'setup/static')
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'setup/static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações para armazenar mensagens na sessão com expiração de 15 segundos
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MESSAGE_TIMEOUT = 15

# Configuração de cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache'),
    }
}

# Configurações de e-mail (substitua pelas suas configurações)
EMAIL_USE_SSL = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "voculary.projeto@gmail.com"
EMAIL_HOST_PASSWORD = "tdlj amtt eiae gglb"

# Adicionar barra final às URLs
APPEND_SLASH = True