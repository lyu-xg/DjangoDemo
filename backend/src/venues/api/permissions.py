from django.conf import settings
from rest_framework.permissions import BasePermission
from venues.models import Venue
from .exceptions import *

class IsAdminOrIsPoster(BasePermission):
    def has_object_permission(self, request, view, obj):
    	if request.user.is_staff or request.user.is_superuser:
    	    return True
    	if isinstance(obj, Venue):
    	    if obj.poster == request.user:
		        return True

        raise ETP0001