from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from _abstract.api.viewsets.mixins import MultiSerializerViewSetMixin
from venues.models import *
from shows.models import *
from .serializers import *


class VenueViewSet(
        MultiSerializerViewSetMixin,
        viewsets.mixins.CreateModelMixin,
        viewsets.mixins.ListModelMixin,
        viewsets.mixins.RetrieveModelMixin,
        viewsets.mixins.UpdateModelMixin,
        viewsets.mixins.DestroyModelMixin,
        viewsets.GenericViewSet):

	queryset = Venue.objects.all()
	serializer_class = VenueSerializer

	ordering_fields = ('created', 'family-friendly')
	search_fields = ('name', 'poster', 'location')
	ordering = ('-created',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_permissions(self):
        # Your logic should be all here
		if self.request.method in ['PUT', 'PATCH', 'DELETE']:
			self.permission_classes = self.permission_classes + \
				(IsAdminOrIsPoster)
		return super().get_permissions()

	def get_venue(self, request, pk=None):
		venue = get_object_or_404(Venue, pk=pk)
		self.venue = venue
		return self.venue

	def create(self, request):
		poster = request.user
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(poster=poster)
		return Response(serializer.data)

class MyRecommandShowsListViewSet(
		viewsets.mixins.ListModelMixin,
		viewsets.GenericViewSet):
	
	queryset = Show.objects.all()
	serializer_class = MyRecommandShowsListSerializer
	permission_classes = (IsAuthenticated,)
	filter_backends = (filters.OrderingFilter,)
	ordering_fields = ('venues')
	ordering = ('-created',)
	def get_queryset(self):
		user_venues = Venue.objects.filter(poster=self.request.user)

		print("user's venues: ", user_venues)

		all_shows = Show.objects.all()
		print("All shows: ", all_shows)

		shows_based_on_location = all_shows.filter(city=self.request.user.city, 
								 state=self.request.user.state)
		print("1: ", shows_based_on_location)

		if len(shows_based_on_location) == 0:
			shows_based_on_location = all_shows.objects.filter(state=self.request.user.state)
		print("2: ", shows_based_on_location)		
		
		return shows_based_on_location