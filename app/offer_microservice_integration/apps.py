"""Django app module for Offer microservice integration."""

# std
import importlib

# third-party
from django.apps import AppConfig


class MicroserviceIntegrationConfig(AppConfig):
    """Django app for Offer microservice integration."""

    name = 'app.offer_microservice_integration'

    def ready(self):
        """Import app signals."""
        super().ready()
        importlib.import_module(".signals", self.name)
