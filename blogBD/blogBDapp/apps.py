from django.apps import AppConfig


class BlogbdappConfig(AppConfig):
    name = 'blogBDapp'
    def ready(self) -> None:
        import blogBDapp.signal
