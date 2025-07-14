from django.contrib import admin  # Importa o painel de administração do Django
from django.urls import path, include  # Importa funções para definir URLs e incluir URLs de outros apps
from django.conf import settings  # Importa as configurações do projeto
from django.conf.urls.static import static  # Importa função para servir arquivos de mídia (imagens, etc.)

urlpatterns = [
    # Rota para acessar o painel de administração do Django (ex: http://localhost:8000/admin/)
    path('admin/', admin.site.urls),
    
    # Inclui as rotas definidas no app "Pages" na raiz do site
    path('', include('Pages.urls')),

]

# Adiciona suporte para servir arquivos enviados pelo usuário (como imagens) durante o desenvolvimento
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
