from django.shortcuts import render
from rest_framework import viewsets
from .models import Aluno
from .serializers import AlunoSerializer

#viewset que permite criar, ler, atualizar e deletar objetos Aluno
class AlunoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Alunos via API REST.
    """
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    