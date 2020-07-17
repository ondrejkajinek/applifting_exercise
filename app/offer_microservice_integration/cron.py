"""Cronjobs for Offer microservice integration app."""

# std
import time

# third-party
from django.conf import settings
from django.db import transaction
from django.db.models import Max
from django.utils import timezone

# local
from api.product.models import Product, Offer, Price
from product_aggregator.utils import setup_cron_logger
from .client import OfferMicroserviceClient


log = setup_cron_logger(
    "app.offer_microservice_integration.cron",
    settings.CRON_LOG_FILES["app.offer_microservice_integration"]
)


def update_offers():
    """Update stock count and price for all offers, get new offers."""
    start = time.perf_counter_ns()
    log.info("Starting cronjob 'update_offer'")
    client = OfferMicroserviceClient()
    for product in Product.objects.all():
        for offer in client.product_offers(product.id):
            try:
                _process_offer(product, offer)
            except BaseException:
                log.error(
                    "Product %d (%s): failed to update / create offer %r",
                    product.id, product, offer
                )

    end = time.perf_counter_ns()
    log.info(
        "Cronjob 'update_offers' finished, it took %.6f ms",
        (end - start) / 1000000
    )


def _create_offer(product, offer_data):
    with transaction.atomic():
        offer = Offer.objects.create(
            external_id=offer_data["id"],
            items_in_stock=offer_data["items_in_stock"],
            product=product
        )
        Price.objects.create(
            timestamp_from=0,
            price=offer_data["price"],
            offer=offer
        )


def _process_offer(product, offer):
    try:
        _update_offer(offer)
    except Offer.DoesNotExist:
        _create_offer(product, offer)


def _update_offer(offer_data):
    with transaction.atomic():
        offer = Offer.objects.prefetched().get(external_id=offer_data["id"])
        offer.items_in_stock = offer_data["items_in_stock"]
        offer.save()

        try:
            current_price = offer.prices.current()
        # no active price, this should not happen
        except Price.DoesNotExist:
            max_timestamp_to = (
                Price.objects
                .aggregate(max_timestamp_to=Max("timestamp_to"))
            )["max_timestamp_to"]
            Price.objects.create(
                # if no Price exists, max_timestamp_to is None
                timestamp_from=max_timestamp_to or 0,
                price=offer_data["price"],
                offer=offer
            )
        else:
            if current_price.price != offer_data["price"]:
                # stop old price
                current_timestamp = int(timezone.now().timestamp())
                current_price.timestamp_to = current_timestamp
                current_price.save()

                # create new one
                Price.objects.create(
                    timestamp_from=current_timestamp,
                    price=offer_data["price"],
                    offer=offer
                )
            # price didn't changed, do nothing
