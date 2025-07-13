from rest_framework import serializers
from .models import Organizacao

class OrganizacaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Organizacao.
    Inclui todos os campos do modelo Organizacao.
    """
    class Meta:
        model = Organizacao
        fields = '__all__'  