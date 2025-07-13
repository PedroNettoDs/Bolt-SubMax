# urls.py (do app ou do projeto)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlunoViewSet

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Ex: /api/alunos/
]
