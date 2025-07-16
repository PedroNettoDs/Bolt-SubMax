from rest_framework import viewsets
from Pages.models import Exercicio, GrupoMuscular
from Pages.serializers import ExercicioSerializer, GrupoMuscularSerializer

class ExercicioViewSet(viewsets.ModelViewSet):
    queryset = Exercicio.objects.all()
    serializer_class = ExercicioSerializer

class GrupoMuscularViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GrupoMuscular.objects.all()
    serializer_class = GrupoMuscularSerializer