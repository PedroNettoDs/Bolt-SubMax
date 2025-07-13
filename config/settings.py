import os
from pathlib import Path

# Define a pasta principal do projeto (a raiz), útil para localizar outras pastas ou arquivos
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta usada pelo Django para segurança interna (como criptografar cookies)
SECRET_KEY = 'django-insecure-2des=jhc@)*%x0%g044db%1claq&ucn!_um1d%%%-fa%t@r6kp'

# Quando True, mostra mensagens de erro detalhadas (usar False em produção)
DEBUG = True

# Lista de domínios permitidos para acessar o site. Vazia significa que só pode acessar localmente
ALLOWED_HOSTS = []


# Aplicativos que estão ativados no seu projeto
INSTALLED_APPS = [
    'django.contrib.admin', # Área administrativa do Django
    'django.contrib.auth',  # Sistema de autenticação (login, usuários)
    'django.contrib.contenttypes',  # Permite trabalhar com tipos de conteúdo genéricos
    'django.contrib.sessions',  # Salva dados de sessão dos usuários
    'django.contrib.messages',  # Permite mostrar mensagens ao usuário
    'django.contrib.staticfiles',   # Lida com arquivos estáticos como CSS e JS

    # Apps do projeto
    'core',  # App principal do projeto
    'organizacao',  # App para gerenciar organizações e autenticação por CPF
    'alunos',  # App para gerenciar alunos
    'agendas',  # App para gerenciar agendamentos
    'treinos',  # App para gerenciar avaliações
    'exercicios',  # App para gerenciar exercícios
    'avaliacao',  # App para gerenciar avaliações

    # Apps de terceiros
    'rest_framework',  # Framework para criar APIs RESTful
]

# Lista de ferramentas que processam as requisições e respostas (como filtros automáticos)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',    # Proteções básicas de segurança
    'django.contrib.sessions.middleware.SessionMiddleware', # Gerencia sessões dos usuários
    'django.middleware.common.CommonMiddleware',    # Funções básicas de requisição/resposta
    'django.middleware.csrf.CsrfViewMiddleware',    # Protege contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Identifica o usuário logado
    'django.contrib.messages.middleware.MessageMiddleware', # Permite usar mensagens temporárias
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Protege contra cliques maliciosos
    'organizacao.middleware.LoginRequiredMiddleware',  # Middleware personalizado para exigir login
    'core.middleware.OrganizacaoMiddleware',  # Middleware personalizado para definir organização
]

# Define o arquivo principal de URLs do projeto
ROOT_URLCONF = 'config.urls'

# Configura o sistema de templates (HTMLs dinâmicos)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',   # Motor de templates do Django
        'DIRS': [], # Lista de pastas onde o Django procura templates (vazia aqui)
        'APP_DIRS': True,   # Procura automaticamente templates dentro de cada app
        'OPTIONS': {
            'context_processors': [ # Informações adicionais que serão incluídas nos templates
                'django.template.context_processors.debug',  # Inclui variáveis de debug
                'django.template.context_processors.request',  # Inclui o objeto da requisição
                'django.contrib.auth.context_processors.auth',  # Informações do usuário logado
                'django.contrib.messages.context_processors.messages',  # Mensagens temporárias
                'django.template.context_processors.media',  # Acesso a arquivos de mídia
            ],
        },
    },
]

# Aponta para o arquivo que inicia o aplicativo web (usado por servidores)
WSGI_APPLICATION = 'config.wsgi.application'


# Configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Tipo de banco (aqui, SQLite)
        'NAME': BASE_DIR / 'db.sqlite3',    # Caminho do arquivo do banco de dados
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
    'organizacao.authentication.CPFBackend',
    'django.contrib.auth.backends.ModelBackend',  # Fallback opcional
]

LOGIN_URL = '/login/'  # URL para a página de login
LOGIN_REDIRECT_URL = '/'  # URL para redirecionar após login bem-sucedido
LOGOUT_REDIRECT_URL = '/'  # URL para redirecionar após logout

# Configurações de localização e idioma

LANGUAGE_CODE = 'pt-br' 
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Configurações de arquivos estáticos (CSS, JS, imagens)
STATIC_URL = 'static/'

# Pasta onde os arquivos estáticos serão coletados (usado em produção)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Tipo padrão para campos de ID no banco de dados (usado ao criar modelos)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configura onde os arquivos enviados (uploads) serão salvos e acessados
MEDIA_URL = '/media/'  # Caminho público para acessar os arquivos
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Pasta onde os arquivos são armazenados