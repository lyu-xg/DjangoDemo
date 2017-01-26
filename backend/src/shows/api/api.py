from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from _abstract.api.viewsets.mixins import MultiSerializerViewSetMixin
from shows.models import *
from venues.models import *
from .serializers import *


class ShowViewSet(
        MultiSerializerViewSetMixin,
        viewsets.mixins.CreateModelMixin,
        viewsets.mixins.ListModelMixin,
        viewsets.mixins.RetrieveModelMixin,
        viewsets.mixins.UpdateModelMixin,
        viewsets.mixins.DestroyModelMixin,
        viewsets.GenericViewSet):

	queryset = Show.objects.all()
	serializer_class = ShowSerializer

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

	def get_show(self, request, pk=None):
		show = get_object_or_404(Show, pk=pk)
		self.show = show
		return self.show

	def create(self, request):
		poster = request.user
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(poster=poster)
		return Response(serializer.data)

class MyRecommandVenuesListViewSet(
		viewsets.mixins.ListModelMixin,
		viewsets.GenericViewSet):
	
	queryset = Venue.objects.all()
	serializer_class = MyRecommandVenuesListSerializer
	permission_classes = (IsAuthenticated,)
	filter_backends = (filters.OrderingFilter,)
	ordering_fields = ('venues')
	ordering = ('-created',)
	def get_queryset(self):
		user_shows = Show.objects.filter(poster=self.request.user)

		print("user's show: ", user_shows)

		all_venues = Venue.objects.all()
		print("All venues: ", all_venues)

		venues_based_on_location = all_venues.filter(city=self.request.user.city, 
								 state=self.request.user.state)
		print("1: ", venues_based_on_location)

		if len(venues_based_on_location) == 0:
			venues_based_on_location = Venue.objects.filter(state=self.request.user.state)
		print("2: ", venues_based_on_location)		
		
		return venues_based_on_location









