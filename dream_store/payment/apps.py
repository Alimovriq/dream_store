from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
    verbose_name = 'Управленние транзакциями'

    def ready(self) -> None:
        import payment.signals
