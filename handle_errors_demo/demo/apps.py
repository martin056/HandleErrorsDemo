from django.apps import AppConfig


class DemoConfig(AppConfig):
    name = 'demo'

    def ready(self):
        import demo.tasks  # noqa