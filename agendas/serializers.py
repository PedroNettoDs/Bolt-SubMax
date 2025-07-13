from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from .models import Agenda

class AgendaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Agenda.
    Inclui todos os campos do modelo Agenda.
    """

    class Meta:
        model = Agenda
        fields = "__all__"

    def validate(self, attrs):
        """
        Reflete a mesma regra de clean() para API.
        """
        instance = Agenda(**attrs)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return attrs
    

class AgendaEventSerializer(serializers.ModelSerializer):
    """
    Serializer para eventos de Agenda.
    """
    # campos calculados que o calendário usa
    start = serializers.SerializerMethodField()
    end   = serializers.SerializerMethodField()
    
    # Combina data + hora e devolve ISO-8601 (timezone-aware) -> necessário para o fullcalendar
    def _build_dt(self, data, hora):
        """
        Combina data e hora em um datetime timezone-aware.
        """
        dt_naive = datetime.combine(data, hora)                  # 2025-07-13 09:00:00
        return timezone.make_aware(dt_naive)                     # 2025-07-13T09:00:00-03:00

    def get_start(self, obj):
        """
        Retorna o horário de início formatado como ISO-8601.
        """
        return self._build_dt(obj.data, obj.hora_inicio).isoformat()

    def get_end(self, obj):
        """
        Retorna o horário de término formatado como ISO-8601.
        """
        return self._build_dt(obj.data, obj.hora_fim).isoformat()