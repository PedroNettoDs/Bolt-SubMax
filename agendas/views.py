from django.shortcuts import render
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from .models import Agenda
from .serializers import AgendaSerializer, AgendaEventSerializer

class AgendaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Agendas via API REST.
    """
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

class AgendaCalendarFeed(ListAPIView):
    """
    API para alimentar o calendário com eventos de Agenda.
    Utiliza o serializer AgendaEventSerializer para formatar os dados.
    """
    serializer_class = AgendaEventSerializer

    def get_queryset(self):
        # FullCalendar envia ?start=2025-07-01&end=2025-07-31
        qs = Agenda.objects.all()
        start = self.request.query_params.get("start")
        end   = self.request.query_params.get("end")
        if start and end:
            qs = qs.filter(data__range=[start, end])
        return qs
    
def calendar_events(request):
    qs = Agenda.objects.all()
    events = []
    for a in qs:
        events.append({
            "id":    a.id,
            "title": a.titulo,
            "start": timezone.make_aware(datetime.combine(a.data, a.hora_inicio)).isoformat(),
            "end":   timezone.make_aware(datetime.combine(a.data, a.hora_fim)).isoformat(),
            "extendedProps": {"descricao": a.descricao, "tipo": a.tipo},
        })
    return JsonResponse(events, safe=False)