# Define URL patterns that later will be included in the application
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .api import (VenueViewSet, MyRecommandShowsListViewSet)

router = DefaultRouter()
router.register(r'venues', VenueViewSet)
router.register(r'me/recommand_shows', MyRecommandShowsListViewSet)

urlpatterns = router.urls
