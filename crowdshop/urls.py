from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from crowdshop import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^tasks/$', views.TaskViewSet.as_view({"get":"list", "post":"create"}), name='tasks'),
	url(r'^tasks/(?P<pk>[0-9]+)/$', views.TaskViewSet.as_view({"get":"retrieve", "patch":"update"}), name='task-detail'),
	url(r'^auth', views.auth, name='auth'),
)
