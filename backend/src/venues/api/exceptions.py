from _abstract.api.exceptions import (PermissionCodeError, BusinessLogicError,
                                     InternalInfoMixin)
from django.conf import settings

class ETP0001(InternalInfoMixin, PermissionCodeError):
    message = "You should be either admin or owner of the post to perform this action"