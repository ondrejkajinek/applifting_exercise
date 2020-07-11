"""Client module for Offer microservice."""

# std
import logging
import urllib.parse

# third-party
import requests
from cached_property import cached_property
from django.conf import settings

# local
from .exceptions import MissingAPIToken
from .models import Configuration


log = logging.getLogger("app.offer_microservice_integration.utils")


EXCEPTIONS = {
    201: None,
    400: RuntimeError,
    401: RuntimeError,
    404: RuntimeError
}


class OfferMicroserviceClient:
    """Client for Offer microservice."""

    TOKEN_KEY = "api_token_key"

    @cached_property
    def api_key(self):
        """Obtain API key for Offer microservice."""
        try:
            api_key = self._load_auth_token()
        except Configuration.DoesNotExist:
            api_key = self._request_auth_token()
            Configuration.objects.create(
                key=self.TOKEN_KEY,
                value=api_key
            )

        return api_key

    def product_offers(self, product_id):
        """Load existing offers for product."""
        return self._call_authorized(
            requests.get,
            "/products/{}/offers".format(product_id)
        )

    def register_product(self, product):
        """Register product in Offer microservice."""
        return self._call_authorized(
            requests.post,
            "/products/register",
            {
                "id": product.id,
                "name": product.name,
                "description": product.description
            }
        )

    def _call_authorized(self, method, resource_path, params=None):
        method_params = {
            "url": urllib.parse.urljoin(
                settings.OFFER_MICROSERVICE_URL, resource_path
            ),
            "headers": {
                "Bearer": self.api_key,
            }
        }
        if params is not None:
            method_params["json"] = params

        resp = method(**method_params)
        if resp.status_code != 201:
            try:
                exception = EXCEPTIONS[resp.status_code]
                message = resp.json()["msg"]
            except (KeyError, ValueError):
                log.error(
                    "Unrecongized response from Offer microservice: %d: %s",
                    resp.status_code, resp.text
                )
                # TODO: exception!
                raise RuntimeError(
                    "Offer microservice gave unrecognized response"
                )

            raise exception(message)

        try:
            response = resp.json()
        except ValueError:
            log.error(
                "Malformed response from Offer microservice: %r", resp.text
            )
            # TODO: exception!
            raise RuntimeError("Offer microservice gave malformed response")

        return response

    def _load_auth_token(self):
        return Configuration.objects.get(key=self.TOKEN_KEY).value

    def _request_auth_token(self):
        print("Requesting api key")
        raise RuntimeError("I wanna break it")
        url = urllib.parse.urljoin(settings.OFFER_MICROSERVICE_URL, "/auth")
        resp = requests.post(url)
        try:
            resp.raise_for_status()
            return resp.json()["access_token"]
        except (KeyError, ValueError):
            log.error("Bad response from Offer MS API: %r", resp.text)
            raise MissingAPIToken("Unexpected response from service")
        except requests.exceptions.HTTPError:
            log.exception("Failed to request auth token")
            raise MissingAPIToken("Auth request failed")
