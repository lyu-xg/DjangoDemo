# CustomUser API
# Apples and Oranges
# Created by Patrick Zhang on 5/9/16
# Copyright © 2016 Patrick Zhang. All rights reserved.

from djoser import views
from djoser import signals
from datetime import datetime
from django.db.models import Q
from django.db.models.signals import post_save, post_delete, pre_save
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from djoser.views import ActivationView
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import detail_route, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from .serializers import *
from _abstract.api.viewsets.mixins import MultiSerializerViewSetMixin, CustomErrorMessagesMixin
from users.models import AppUser
from django.contrib.auth.tokens import default_token_generator


def encode_uid(pk):
    try:
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        return urlsafe_base64_encode(force_bytes(pk)).decode()
    except ImportError:
        from django.utils.http import int_to_base36
        return int_to_base36(pk)

class CustomLoginView(views.LoginView):
    serializer_class = CustomLoginSerializer

    def get_serializer_class(self):
        return CustomLoginSerializer

    def action(self, serializer):
        self.user = serializer.user
        Token.objects.filter(user=self.user).delete()
        return super().action(serializer)


class CustomRegistrationView(views.RegistrationView):
    serializer_class = CustomUserRegistrationSerializer

    def get_serializer_class(self):
        return CustomUserRegistrationSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        token = default_token_generator.make_token(instance)
        uid = encode_uid(instance.pk)
        print("IN CustomRegistrationView: uid/token: ")
        print("activate/{}/{}\n\n".format(uid,token))
        signals.user_registered.send(
            sender=self.__class__, user=instance, request=self.request)
        # self.post_save(obj=instance, created=True)


class CustomUserView(views.UserView):
    serializer_class = CustomUserSerializer


class CustomSetUsernameView(views.SetUsernameView):
    serializer_class = CustomSetUsernameSerializer

    def get_serializer_class(self):
        return CustomSetUsernameSerializer


class CustomSetPasswordView(views.SetPasswordView):
    serializer_class = CustomSetPasswordSerializer

    def get_serializer_class(self):
        return CustomSetPasswordSerializer


class CustomPasswordResetView(views.PasswordResetView):
    serializer_class = CustomPasswordResetSerializer

    def get_serializer_class(self):
        return CustomPasswordResetSerializer


class UserProfilesViewSet(
    MultiSerializerViewSetMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):

    queryset = AppUser.objects.all()
    serializer_class = UserProfileSerializer

    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('date_joined',)
    search_fields = ('first_name', 'last_name', )
    ordering = ('date_joined',)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        return Response(status=status.HTTP_200_OK)

class CustomActivationView(ActivationView):
    def action(self, serializer):
        serializer.user.is_email_verified = True
        return super().action(serializer)
