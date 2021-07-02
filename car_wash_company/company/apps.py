from django.apps import AppConfig


class CompanyConfig(AppConfig):
    name = 'company'

    def ready(self) -> None:
        import company.signals
