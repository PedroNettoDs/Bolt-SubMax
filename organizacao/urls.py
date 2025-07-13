from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import organizacaoViewSet

router = DefaultRouter()
router.register(r'organizacoes', organizacaoViewSet)

urlpatterns = [
    path("", include(router.urls)),  # Ex: /api/organizacoes/
]