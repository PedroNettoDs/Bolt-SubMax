from django.apps import AppConfig


class ExerciciosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exercicios'
    label = 'exercicios'        # corresponde ao check no signal

    def ready(self):
        # importa para acionar o decorador @receiver
        from . import signals  # noqa