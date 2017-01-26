from django.conf import settings
from rest_framework.permissions import BasePermission
from shows.models import Show
from .exceptions import *


class IsAdminOrIsPoster(BasePermission):
    def has_object_permission(self, request, view, obj):
    	if request.user.is_staff or request.user.is_superuser:
    	    return True
    	if isinstance(obj, Show):
    	    if obj.poster == request.user:
		        return True

        raise ETP0001

class IsPosterShowManager(BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.user.role == 'S':
			return True
			
		raise ETP0002