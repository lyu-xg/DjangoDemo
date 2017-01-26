import json
from django.contrib import admin
from django.contrib.admin import helpers
from django.template.response import TemplateResponse
from django.utils.text import Truncator
from django_object_actions import (DjangoObjectActions,
                                   takes_instance_or_queryset)
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from _abstract.admin.mixins import (NonEditableInline, FkAdminLink,)

from .models import Show

class ShowAdmin(DjangoObjectActions, FkAdminLink,
                admin.ModelAdmin):
	list_filter = ('genre', )
	search_fields = ('location', 'name', 'genre',)

	list_display = ('id', 'name')

admin.site.register(Show, ShowAdmin)
