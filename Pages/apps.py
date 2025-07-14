from django.apps import AppConfig
from django.db.models.signals import post_migrate 

class PaginasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Pages'
    verbose_name = 'Meu App de Páginas'

    def ready(self):
        from .signals import criar_plano_padrao
        post_migrate.connect(criar_plano_padrao, sender=self)