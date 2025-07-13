from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import avaliacaoViewSet

router = DefaultRouter()
router.register(r'avaliacoes', avaliacaoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Ex: /api/avaliacoes/
]