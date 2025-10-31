from django.apps import AppConfig


class GraderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'grader'

    def ready(self):
        import grader.models  # Importar para que los signals funcionen
