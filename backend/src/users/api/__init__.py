# Define URL patterns that later will be included in the application
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()

# router.register(r'users', UserProfilesViewSet)

urlpatterns = router.urls
urlpatterns.append(url(r'^auth/me/$', CustomUserView.as_view(), name='user'))
urlpatterns.append(url(r'^auth/register/$', CustomRegistrationView.as_view(), name='register'))
urlpatterns.append(url(r'^auth/{}/$'.format(User.USERNAME_FIELD), CustomSetUsernameView.as_view(), name='set_username'))
urlpatterns.append(url(r'^auth/activate/$', CustomActivationView.as_view(),
                       name='activate'))
urlpatterns.append(url(r'^auth/password/$', CustomSetPasswordView.as_view(), name='set_password'))
urlpatterns.append(url(r'^auth/password/reset/$', CustomPasswordResetView.as_view(), name='password_reset'))
urlpatterns.append(url(r'^auth/login/$', CustomLoginView.as_view(), name='login'))