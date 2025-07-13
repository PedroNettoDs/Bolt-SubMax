from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExercicioViewSet

router = DefaultRouter()
router.register(r'exercicios', ExercicioViewSet)

urlpatterns = [
    path("", include(router.urls)), # Ex: /api/exercicios/
]