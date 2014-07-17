from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views

from crowdshop import views


urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^api/$', views.api_root, name='api_root'),
	url(r'^users/$', views.UserList.as_view(), name='userlist'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='userdetail'),
	url(r'^tasks/$', views.TaskList.as_view(), name='tasklist'),
	url(r'^tasks/(?P<pk>[0-9]+)/$', views.TaskDetail.as_view(), name='taskdetail'),
	url(r'^claim/$', views.claimTask, name='claimtask'),
	url(r'^create_task', views.create_task, name="create_task"),
	url(r'^claim_task', views.claim_task, name="claim_task"),
	url(r'^pay_task', views.pay_task, name="pay_task"),
	url(r'^auth', views.auth, name='auth'),
)
