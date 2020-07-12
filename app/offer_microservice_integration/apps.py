"""Django app module for Offer microservice integration."""

# third-party
from django.apps import AppConfig


class MicroserviceIntegrationConfig(AppConfig):
    """Django app for Offer microservice integration."""

    name = 'app.offer_microservice_integration'

    def ready(self):
        super().ready()
        from . import signals
