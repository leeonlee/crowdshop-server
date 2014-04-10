from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views

from crowdshop import views


urlpatterns = patterns('',
	url(r'^$', views.api_root, name='api_root'),
	url(r'^users/$', views.UserList.as_view(), name='userlist'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='userdetail'),
	url(r'^tasks/$', views.TaskList.as_view(), name='tasklist'),
)
