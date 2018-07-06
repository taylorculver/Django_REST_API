from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from . import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', views.UserRegisterView.as_view(),
        name='register-user'),

    # To get all dogs (not used in application)
    url(r'^api/dogs/$', views.AllDogs.as_view(), name='all-dogs'),

    # To get a dog (not used in application)
    url(r'^api/dog/(?P<pk>-?\d+)/$', views.SpecificDog.as_view(),
        name='specific-dog'),

    # To get the next liked/disliked/undecided dog
    url(r'^api/dog/(?P<pk>-?\d+)/'
        r'(?P<decision>liked|disliked|undecided)/next/$',
        views.GETNextDog.as_view(),
        name='next'),

    # To change the dog's status
    url(r'^api/dog/(?P<pk>-?\d+)/(?P<decision>liked|disliked|undecided)/$',
        views.PUTUserDog.as_view(),
        name='decide'),

    # To change or set user preferences
    url(r'^api/user/preferences/$',
        views.GETorPUTUserPref.as_view(),
        name='userpref'),

    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html'))
])
