# CustomUser Serializer
# Apples and Oranges
# Created by Patrick Zhang on 5/9/16
# Copyright © 2016 Patrick Zhang. All rights reserved.


from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from djoser.serializers import *
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from _abstract.api.viewsets.mixins import CustomErrorMessagesMixin
from _abstract.api.serializers.fields import DateTimeFieldWihTZ
from _abstract.api.serializers import mixins
from _abstract.api.exceptions import BusinessLogicError
 
User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
 
    def validate(self, attrs):
        self.user = authenticate(username=attrs[User.USERNAME_FIELD], password=attrs['password'])
        if self.user:
            if not self.user.is_active:
                raise UTP0002_SUSPENDED_ACCOUNT
            return attrs
        else:
            raise UTP0001_INVALID_LOGIN
 
    def to_internal_value(self, data):
        """
        This is solution to avoid case sensitive usernames/emails during login as Django's case sensitivenes is something
        they don't want to get rid of due to legacy issues
        :param data:
            submitted attributed
        :return:
            attributes where USERNAME_FIELD value is lowecase
        """
        if data.get(User.USERNAME_FIELD, None):
            data[User.USERNAME_FIELD]=data[User.USERNAME_FIELD].lower()
        return super().to_internal_value(data)
 
class CustomUserRegistrationSerializer(
        CustomErrorMessagesMixin,
        UserRegistrationSerializer):
 
    class Meta:
        model = User
        fields = UserRegistrationSerializer.Meta.fields + ('role', 'email', 'city', 'state')
        write_only_fields = ('password',)
 
        custom_error_messages_for_validators = {
            'username': {
                UniqueValidator: _('This username is already being used, please select another one'),
            },
        }
 
    def to_internal_value(self, data):
        """
        This is solution to avoid case sensitive usernames/emails during login as Django's case sensitivenes is something
        they don't want to get rid of due to legacy issues
        :param data:
            submitted attributed
        :return:
            attributes where USERNAME_FIELD value is lowecased
        """
        if data.get(User.USERNAME_FIELD, None):
            data[User.USERNAME_FIELD] = data[User.USERNAME_FIELD].lower()
        return super().to_internal_value(data)
 
 
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User._meta.pk.name,
            User.USERNAME_FIELD,
        ) + User.CUSTOM_FIELDS
        read_only_fields = User.READ_ONLY_FIELDS
 
 
class CustomSetUsernameSerializer(mixins.ValidationErrorMixin, SetUsernameSerializer):
    pass
 
 
class CustomSetPasswordSerializer(mixins.ValidationErrorMixin, SetPasswordSerializer):
    default_detail = ''
    default_error_messages = {
        'invalid_password': 'You provided incorrect current password',
    }
 
 
class CustomPasswordResetSerializer(mixins.ValidationErrorMixin, PasswordResetSerializer):
    pass
 
 
class UserProfileSerializer(serializers.ModelSerializer):
 
    date_joined = DateTimeFieldWihTZ(read_only=True)
 
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 
                  'role', 'address1', 'address2', 'city', 'state', 'zip_code', 'country')