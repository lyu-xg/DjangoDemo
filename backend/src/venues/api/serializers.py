from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from _abstract.api.serializers import mixins
from _abstract.api.serializers.fields import DateTimeFieldWihTZ, MonthYearField
from venues.models import *
from shows.models import *

User = get_user_model()

class VenueUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'role',
                  'location',)

class VenueSerializer(mixins.UnknownFieldsValidationMixin, 
                     serializers.ModelSerializer):
    poster = VenueUserSerializer(read_only=True)
    created = DateTimeFieldWihTZ(read_only=True)
    updated = DateTimeFieldWihTZ(read_only=True)
    family_friendly = serializers.BooleanField()
    
    class Meta:
        model = Venue
        fields = ('id',
                  'name',
                  'city',
                  'state',
                  'duration',
                  'genre',
                  'family_friendly',
                  'space',
                  'description',
                  'poster',
                  'created',
                  'updated',)
        read_only_fields = ('created','updated')

class MyRecommandShowsListSerializer(serializers.Serializer):
    name = serializers.CharField()
    poster = VenueUserSerializer(read_only=True)
    location = serializers.CharField()
    genre = serializers.CharField()
    family_friendly = serializers.BooleanField()
    crew_size = serializers.IntegerField()