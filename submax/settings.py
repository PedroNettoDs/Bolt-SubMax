import os  # Biblioteca para interagir com o sistema de arquivos
from pathlib import Path  # Biblioteca moderna para lidar com caminhos de arquivos


# Define a pasta principal do projeto (a raiz), útil para localizar outras pastas ou arquivos
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta usada pelo Django para segurança interna (como criptografar cookies)
SECRET_KEY = 'django-insecure-@1kftgb#nrvvrsc_npqvxz^ro1)t(83!z0i#nctw+l080f5zl2'

# Quando True, mostra mensagens de erro detalhadas (usar False em produção)
DEBUG = True

# Lista de domínios permitidos para acessar o site. Vazia significa que só pode acessar localmente
ALLOWED_HOSTS = []

# Aplicativos que estão ativados no seu projeto
INSTALLED_APPS = [
    'django.contrib.admin',  # Área administrativa do Django
    'django.contrib.auth',  # Sistema de autenticação (login, usuários)
    'django.contrib.contenttypes',  # Permite trabalhar com tipos de conteúdo genéricos
    'django.contrib.sessions',  # Salva dados de sessão dos usuários
    'django.contrib.messages',  # Permite mostrar mensagens ao usuário
    'django.contrib.staticfiles',  # Lida com arquivos estáticos como CSS e JS
    'Pages',  # Outro aplicativo do seu projeto

    # Apps de terceiros
    'rest_framework',  # Framework para criar APIs RESTful
]

# Lista de ferramentas que processam as requisições e respostas (como filtros automáticos)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Proteções básicas de segurança
    'django.contrib.sessions.middleware.SessionMiddleware',  # Gerencia sessões dos usuários
    'django.middleware.common.CommonMiddleware',  # Funções básicas de requisição/resposta
    'django.middleware.csrf.CsrfViewMiddleware',  # Protege contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Identifica o usuário logado
    'django.contrib.messages.middleware.MessageMiddleware',  # Permite usar mensagens temporárias
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protege contra cliques maliciosos
    'Pages.middleware.login_required.LoginRequiredMiddleware',
]

# Define o arquivo principal de URLs do projeto
ROOT_URLCONF = 'submax.urls'

# Configura o sistema de templates (HTMLs dinâmicos)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Motor de templates do Django
        'DIRS': [],  # Lista de pastas onde o Django procura templates (vazia aqui)
        'APP_DIRS': True,  # Procura automaticamente templates dentro de cada app
        'OPTIONS': {
            'context_processors': [  # Informações adicionais que serão incluídas nos templates
                'django.template.context_processors.request',  # Inclui o objeto da requisição
                'django.contrib.auth.context_processors.auth',  # Informações do usuário logado
                'django.contrib.messages.context_processors.messages',  # Mensagens temporárias
            ],
        },
    },
]

# Aponta para o arquivo que inicia o aplicativo web (usado por servidores)
WSGI_APPLICATION = 'submax.wsgi.application'


# Configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Tipo de banco (aqui, SQLite)
        'NAME': BASE_DIR / 'db.sqlite3',  # Caminho do arquivo do banco de dados
    }
}


# Regras para validar senhas seguras
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Verifica se a senha é muito parecida com dados do usuário
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Verifica se a senha tem um tamanho mínimo
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Impede o uso de senhas muito comuns
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Evita senhas que sejam só números
    },
]

# Configurações de autenticação por CPF
AUTHENTICATION_BACKENDS = [
    'Pages.authentication.CPFBackend',
    'django.contrib.auth.backends.ModelBackend',  # Fallback opcional
]

LOGIN_URL = '/login/'  # ou o caminho correto para sua view de login

# Configurações de idioma e fuso horário
LANGUAGE_CODE = 'en-us'  # Idioma padrão do sistema (inglês dos EUA)
TIME_ZONE = 'UTC'  # Fuso horário (pode trocar para 'America/Sao_Paulo' se quiser o horário do Brasil)
USE_I18N = True  # Ativa a tradução de textos do sistema
USE_TZ = True  # Ativa uso de fuso horário

# Configurações para arquivos estáticos como CSS, JavaScript e imagens
STATIC_URL = 'static/'  # URL base para acessar arquivos estáticos

# Pasta onde os arquivos estáticos serão coletados (usado em produção)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Tipo padrão para campos de ID no banco de dados (usado ao criar modelos)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configura onde os arquivos enviados (uploads) serão salvos e acessados
MEDIA_URL = '/media/'  # Caminho público para acessar os arquivos
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Pasta onde os arquivos são armazenados
