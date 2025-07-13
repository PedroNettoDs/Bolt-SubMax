from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alunos.views import AlunoViewSet # Importa o viewset AlunoViewSet
from agendas.views import AgendaViewSet   # Importa o viewset AgendaViewSet


router = DefaultRouter()
router.register(r'alunos', AlunoViewSet)  # Registra o viewset no roteador
router.register(r"agendas", AgendaViewSet)   # Registra o viewset AgendaViewSet no roteador


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls")),  # Inclui as URLs do app core
    path('api/', include("avaliacao.urls")),  # endpoints DRF
    path('api/', include("treinos.urls")),  # endpoints DRF
    path('api/', include("agendas.urls")),  # endpoints DRF
    path("api/", include("alunos.urls")),  # endpoints DRF
    path("api/", include("exercicios.urls")),   #endpoints DRF
    path("api/", include(router.urls)),  # Inclui as URLs do roteador
]
