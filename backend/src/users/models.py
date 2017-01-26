# CustomUser Admin
# Apples and Oranges
# Created by Patrick Zhang on 5/9/16
# Copyright © 2016 Patrick Zhang. All rights reserved.

from django.db import models
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model

# Solution to avoid unique_together for email
AbstractUser._meta.get_field('email')._unique = True

class AppUser(AbstractUser):
    """
    Custom user model for the application
    blank=True means Empty values allowed from the backend, if blank=False, then the field will be required in backend

    """

    _ROLE = (('V', 'Venue'), ('S', 'Show'), )

    role = models.CharField(max_length=1,
                              blank=True,
                              null=True,
                              choices=_ROLE,
                              default='S')
    is_email_verified = models.BooleanField(verbose_name='email verified', 
                                            help_text='Designates whether this user has verified email',
                                            default=False)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=125, null=True, blank=True)
    state = models.CharField(max_length=55, null=True, blank=True)
    zip_code = models.CharField(max_length=5, null=True, blank=True)

    # for DJOSER
    REQUIRED_FIELDS = ['first_name', 'last_name','email']
    # for serializer hack
    READ_ONLY_FIELDS = ('')

    CUSTOM_FIELDS = ('role', 'address1', 'address2', 'city', 'state', 'zip_code')


    def __str__(self):
        return "{}: {}".format(self.id, self.username)

    @property
    def location(self):
        return "{} {} {} {}".format(self.address1.capitalize(),
                                    self.address2.capitalize(),
                                    self.city.capitalize(),
                                    self.state.upper())



# ----------------------------------------------------------------------------------------------------------------------
# Signals
# ----------------------------------------------------------------------------------------------------------------------


@receiver(pre_save, sender=AppUser)
def new_user_created(sender, instance, *args, **kwargs):
    """
    Sets new phone code and email code and SMS / Emails them
    """
    if instance.is_superuser:
        return

    if not instance.id:
        '''
        instance.is_email_verified = False means user needs to verified their email before login.
        instance.is_active = True means user by default is active(not suspended).
        '''
        instance.is_email_verified = False
        instance.is_active = True
