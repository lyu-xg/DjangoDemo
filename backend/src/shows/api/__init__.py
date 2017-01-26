# Define URL patterns that later will be included in the application
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .api import (ShowViewSet, MyRecommandVenuesListViewSet)

router = DefaultRouter()
router.register(r'shows', ShowViewSet)
router.register(r'me/recommand_venues', MyRecommandVenuesListViewSet)

urlpatterns = router.urls
