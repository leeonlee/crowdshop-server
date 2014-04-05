from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views

from crowdshop import views


urlpatterns = patterns('',
	url(r'^login', views.login, name='login'),
)
