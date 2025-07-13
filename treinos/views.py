from django.shortcuts import render
from rest_framework import viewsets
from .models import Rotina
from .serializers import treinoSerializer

class treinoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para treino.
    """
    queryset = Rotina.objects.all()
    serializer_class = treinoSerializer