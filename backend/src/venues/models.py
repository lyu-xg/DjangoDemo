# CustomUser Admin
# Apples and Oranges
# Created by Patrick Zhang on 5/9/16
# Copyright © 2016 Patrick Zhang. All rights reserved.

from django.db import models
from _abstract.models.mixins import CreationModificationMixin
from users.models import AppUser

class Venue(CreationModificationMixin):
    _GENERES =(("Musical", "Musical"),
               ("Opera", "Opera"),
               ("Play", "Play"),
               ("Ballet", "Ballet"),
               ("Classical", "Classical"),
               ("Comedy", "Comedy"),)
    name = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=5, null=True, blank=True)
    duration = models.CharField(max_length=40, null=True, blank=True)
    genre = models.CharField(max_length=20,
                              blank=True,
                              null=True,
                              choices=_GENERES)
    poster = models.ForeignKey(AppUser,
                               verbose_name="Manager",
                               related_name='posted_venue',
                               null=False,
                               blank=False,
                               db_index=True)
    space = models.PositiveSmallIntegerField(null=True,
                                            blank=True,
                                            default=1,
                                            )
    family_friendly = models.BooleanField(null=False, blank=True, default=False)
    description = models.TextField(null=True, blank=False)

    def __str__(self):
        return "{}: {}".format(self.id, self.name)

    @property
    def location(self):
        return "{} {}".format(self.city.capitalize(),
                              self.state.upper())