from django.apps import AppConfig


class Fp10AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fp10_app'

    def ready(self):
        import fp10_app.signals
