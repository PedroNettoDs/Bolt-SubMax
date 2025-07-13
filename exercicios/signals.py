# Signals para criar ou atualizar os músculos fixos após migrações

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import GrupoMuscular
from .constants import MUSCLE_PRESETS

@receiver(post_migrate)
def create_muscles(sender, app_config, **kwargs):
    """
    Depois de cada `migrate`, insere (ou atualiza) os músculos fixos.
    """
    if app_config.label != 'exercicios':   # evita rodar em outros apps
        return

    for slug, nome in MUSCLE_PRESETS.items():
        GrupoMuscular.objects.update_or_create(
            id=slug,
            defaults={'nome': nome}
        )
