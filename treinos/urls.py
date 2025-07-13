from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import treinoViewSet

router = DefaultRouter()
router.register(r'treinos', treinoViewSet)

urlpatterns = [
    path("", include(router.urls)),  # Ex: /api/treinos/
]