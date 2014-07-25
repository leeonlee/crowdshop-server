from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views

from crowdshop import views

urlpatterns = patterns('',
	url(r'^$', views.api_root, name='api_root'),
	url(r'^users/$', views.UserList.as_view(), name='userlist'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='userdetail'),
	url(r'^tasks/$', views.Tasks.as_view(), name='tasks'),
	url(r'^tasks/(?P<pk>[0-9]+)/$', views.TaskDetail.as_view({"get":"retrieve", "patch":"patch"}), name='taskdetail'),
	url(r'^claim_task', views.claim_task, name="claim_task"),
	url(r'^pay_task', views.pay_task, name="pay_task"),
	url(r'^auth', views.auth, name='auth'),
)
