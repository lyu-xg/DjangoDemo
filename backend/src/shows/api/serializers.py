from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from _abstract.api.serializers import mixins
from _abstract.api.serializers.fields import DateTimeFieldWihTZ, MonthYearField
from shows.models import *
from venues.models import *

User = get_user_model()

class ShowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'role',
                  'location',)

class ShowSerializer(mixins.UnknownFieldsValidationMixin,
                     serializers.ModelSerializer):
    poster = ShowUserSerializer(read_only=True)
    created = DateTimeFieldWihTZ(read_only=True)
    updated = DateTimeFieldWihTZ(read_only=True)
    family_friendly = serializers.BooleanField()
#    location = serializers.CharField(max_length=155)

    class Meta:
        model = Show
        fields = ('id',
                  'name',
                  'city',
                  'state',
                  'location',
                  'duration',
                  'genre',
                  'family_friendly',
                  'crew_size',
                  'description',
                  'poster',
                  'created',
                  'updated',)
        read_only_fields = ('created','updated')

class MyRecommandVenuesListSerializer(serializers.Serializer):
    name = serializers.CharField()
    poster = ShowUserSerializer(read_only=True)
    location = serializers.CharField()
    genre = serializers.CharField()
    family_friendly = serializers.BooleanField()
    space = serializers.IntegerField()
