from django.apps import AppConfig


class CustomConfig(AppConfig):
    name = 'app'

    def ready(self):
        import app.signals