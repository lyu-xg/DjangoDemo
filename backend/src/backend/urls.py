# Custom URL endpoints
# Apples and Oranges
# Created by Patrick Zhang on 5/9/16
# Copyright © 2016 Patrick Zhang. All rights reserved.


"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users.api import urlpatterns as users_api_urls
from shows.api import urlpatterns as shows_api_urls
from venues.api import urlpatterns as venues_api_urls
import users.views
import shows.views
import venues.views

urlpatterns = [

    # Admin endpoints
    url(r'^admin/', include(admin.site.urls)),
    # Users endpoints
    url(r'^api/v1/', include(users_api_urls)),
    # Shows endpoints
    url(r'^api/v1/', include(shows_api_urls)),
    # Venues endpoints
    url(r'^api/v1/', include(venues_api_urls)),

    # Home Page (Angular)
    url(r'^$', users.views.index, name='index'),
    # About Page (Angular)
    url(r'^about', users.views.about, name='about'),
    # Page Profile
    url(r'^page-profile', users.views.profile, name='profile'),
    # Show Page (Angular)
    url(r'^shows', shows.views.shows, name='shows'),
    # Venue Page (Angular)
    url(r'^venues', venues.views.venues, name='venues'),
    # Sign In Page (Angular)
    url(r'^signin', users.views.signin, name='signin'),
    # Sign Up Page (Angular)
    url(r'^signup', users.views.signup, name='signup'),
]
