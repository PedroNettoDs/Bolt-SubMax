from django.shortcuts import render
from rest_framework import viewsets
from .models import Exercicio
from .serializers import ExercicioSerializer

class ExercicioViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para exercícios.
    """
    queryset = Exercicio.objects.all()
    serializer_class = ExercicioSerializer