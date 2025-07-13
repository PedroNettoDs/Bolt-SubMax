from django.shortcuts import render
from rest_framework import viewsets
from .models import organizacao
from .serializers import organizacaoSerializer

class organizacaoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para organização.
    """
    queryset = organizacao.objects.all()
    serializer_class = organizacaoSerializer