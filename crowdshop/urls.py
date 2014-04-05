from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views

from crowdshop import views


urlpatterns = patterns('',
	url(r'^loginview', views.loginview, name='loginview'),
	url(r'^createtask', views.createTask, name='createTask'),
    url(r'^tasklist/', TaskList.as_view()),
    url(r'^tasklistother/', TaskListOthers.as_view()),
    url(r'^tasklist/(?P<username>.+)/$', TaskListUser.as_view()),
)
