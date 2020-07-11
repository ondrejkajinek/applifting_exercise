"""URL configuration for Product api."""

# third-party
from rest_framework import routers

# local
from api.product import views

router = routers.SimpleRouter()
router.register("product", views.ProductViewSet, basename="product")
router.register("offer", views.OfferViewSet, basename="offer")

urlpatterns = router.urls
