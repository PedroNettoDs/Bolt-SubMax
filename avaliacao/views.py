from django.shortcuts import render
from rest_framework import viewsets
from .models import Avaliacao
from .serializers import AvaliacaoSerializer

class avaliacaoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Avaliações via API REST.
    """
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer