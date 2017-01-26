# CustomUser Admin
# Apples and Oranges
# Created by Patrick Zhang on 5/9/16
# Copyright © 2016 Patrick Zhang. All rights reserved.
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from djoser import settings as djoser_settings
from djoser.utils import SendEmailViewMixin

from _abstract.admin.mixins import (NonEditableInline, FkAdminLink,)
from .models import AppUser

class CustomUserCreationForm(SendEmailViewMixin, forms.ModelForm):
	"""Form for creating user using admin interface.
	"""
	username = forms.CharField()
	role = forms.CharField()
	address1 = forms.CharField()
	address2 = forms.CharField()
	city = forms.CharField()
	state = forms.CharField()
	zip_code = forms.CharField()

	# settings for Activation email (handled by SendEmailViewMixin from
	# djoser app)
	token_generator = default_token_generator

	class Meta:
		model = AppUser
		fields = ('id', 'username', 'password', 'role', 'address1',
				  'address2', 'city', 'state', 'zip_code')
		widgets = {
				  'password': forms.PasswordInput,
		}


class AppUserAdmin(FkAdminLink, UserAdmin):
	add_form = CustomUserCreationForm
	add_form_template = 'admin/change_form.html'
	list_display = ('id', 'username', 'role', 'address1', 'address2', 'city', 'state', 'zip_code')
	list_filter = ('role', )
	readonly_fields = ('last_login', 'date_joined', )
	list_max_show_all = 1000
	list_per_page = 100
	search_fields = ('email', 'about', 'skills', 'first_name', 'last_name', 'major')
	ordering = ('id', )


admin.site.register(AppUser, AppUserAdmin)


