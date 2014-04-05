from django.conf.urls import patterns, include, url
from rest_framework import routers
from crowdshop import views
from crowdshop.views import TaskList

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'users', views.UserViewSet)

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crowdshop_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(router.urls)),
    url(r'^tasklist/', TaskList.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
)
